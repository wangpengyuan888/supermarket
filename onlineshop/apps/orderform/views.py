import os
import random
from datetime import datetime
from time import sleep

from alipay import AliPay, ISVAliPay
from django.db import transaction
from django.db.transaction import savepoint, savepoint_rollback, savepoint_commit
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django_redis import get_redis_connection
from db.Base_View import VerifyLoginView
from goods.models import GoodsSKU
from orderform.forms import CheckAddressModelForm3
from orderform.models import AddressTable2, Expressage, Order, OrderGoods, Payment
from shopingcar.helper import json_msg

from user.models import UserTable


def alipayfun():
    # 构造支付请求
    app_private_key_string = open(os.path.join(settings.BASE_DIR, 'alipay_key/应用私钥2048.txt')).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay_key/alipay_public_key.txt')).read()
    # 初始化对象
    alipay = AliPay(
        appid="2016092400582448",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    return alipay


# 所有订单页面
class AllOrderClassView(VerifyLoginView):
    def get(self, request):
        return render(request, 'orderform/allorder.html')


# 确认订单
class SureOrder(VerifyLoginView):
    def get(self, request):
        user_id = request.session.get("ID")
        data = AddressTable2.objects.filter(user_id=user_id).order_by('-is_default').first()
        return render(request, 'orderform/tureorder.html', {'data': data})

    def post(self, request):
        # 获取默认收获地址
        user_id = request.session.get("ID")
        data = AddressTable2.objects.filter(user_id=user_id).order_by('-is_default').first()
        # 获取勾选商品的sku_id并把商品信息查找出来
        sku_ids = request.POST.getlist('sku_ids')
        cart_key = f"cart_{user_id}"
        goods = []
        goods_total_price = 0
        r = get_redis_connection()
        for i in sku_ids:
            try:
                good = GoodsSKU.objects.get(pk=i)
            except GoodsSKU.DoesNotExist:
                # 商品不存在就报出异常
                raise Http404('商品不存在请刷新购物车页面重新下单')
            try:
                count = int(r.hget(cart_key, i))
            except:
                raise Http404('商品不存在请刷新购物车页面重新下单')
            good.total = count
            goods.append(good)
            goods_total_price += good.price * count
        expressage = Expressage.objects.filter(is_delete=False).order_by('price')
        context = {
            'data': data,
            'goods': goods,
            'goods_total_price': goods_total_price,
            'expressage': expressage
        }
        return render(request, 'orderform/tureorder.html', context=context)


# 订单信息的保存
class OrderSave(VerifyLoginView):
    def get(self, request):
        pass

    @transaction.atomic
    def post(self, request):
        """
        保存订单数据
        """
        # 接受参数
        user_id = request.session.get('ID')
        user = UserTable.objects.get(pk=user_id)
        address_id = request.POST.get('address_id')
        sku_ids = request.POST.getlist('sku_ids')
        expressage = request.POST.get('expressage')
        # 操作数据
        try:
            address_id = int(address_id)
            expressage = int(expressage)
            sku_ids = [int(i) for i in sku_ids]
        except:
            return JsonResponse(json_msg(9, '参数错误'))
        # 验证收获地址和运输方式是否正确
        try:
            address = AddressTable2.objects.get(pk=address_id)
        except AddressTable2.DoesNotExist:
            return JsonResponse(json_msg(8, '收货地址不存在'))

        try:
            transport = Expressage.objects.get(pk=expressage)
        except Expressage.DoesNotExist:
            return JsonResponse(json_msg(7, '运输方式不存在'))
        order_sn = '{}{}{}'.format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.detail_address)
        # 操作数据库

        # 创建保存点
        sid = savepoint()
        # 1.操作订单基本信息表
        order = Order.objects.create(
            user=user,
            order_sn=order_sn,
            transport_price=transport.price,
            transport=transport.name,
            username=address.user_name,
            phone=address.phone,
            address=address_info
        )
        # 2.操作订单商品表
        r = get_redis_connection()
        cart_key = f"cart_{user_id}"
        goods_total_price = 0
        for sku_id in sku_ids:
            try:
                goods_sku = GoodsSKU.objects.select_for_update().get(pk=sku_id, is_delete=False, is_selling=True)
            except GoodsSKU.DoesNotExist:
                savepoint_rollback(sid)
                return JsonResponse(json_msg(6, '商品不存在'))
            # 获取redis中的商品数量
            try:
                count = int(r.hget(cart_key, sku_id))
            except:
                savepoint_rollback(sid)
                return JsonResponse(json_msg(5, '购物车中数量不存在'))
            # 判断库存是否足够
            if goods_sku.stock < count:
                savepoint_rollback(sid)
                return JsonResponse(json_msg(4, '库存不足'))
            OrderGoods.objects.create(
                order=order,
                good_sku=goods_sku,
                price=goods_sku.price,
                count=count
            )
            goods_total_price += goods_sku.price * count
            # 扣除库存,销量增加
            goods_sku.stock -= count
            goods_sku.sales += count
            goods_sku.save()

        # 3.将订单基本信息表补充完成
        order_total_price = goods_total_price + transport.price
        order.goods_total_price = goods_total_price
        order.order_price = order_total_price
        order.save()

        # 4清空redis中的购物车信息
        r.hdel(cart_key, *sku_ids)
        savepoint_commit(sid)

        # 5合成响应返回
        return JsonResponse(json_msg(0, '创建订单成功', data=order_sn))


# 管理收获地址
class AdminAddressClassView(VerifyLoginView):
    def get(self, request):
        user_id = request.session.get('ID')
        data = AddressTable2.objects.filter(user_id=user_id).order_by('-is_default')
        return render(request, 'orderform/gladdress.html', {'data': data})


# 支付页面
class SurePay(VerifyLoginView):
    def get(self, request):
        order_sn = request.GET.get('order_sn')
        data = Order.objects.get(order_sn=order_sn)
        payment = Payment.objects.all()
        context = {
            'data': data,
            'payments': payment
        }
        return render(request, 'orderform/pay.html', context=context)

    def post(self, request):
        user_id = request.session.get('ID')
        # 接受支付方式的id和订单编号
        try:
            payment = int(request.POST.get('payment'))
            order_sn = request.POST.get('order_sn')
        except:
            return JsonResponse(json_msg(1, '参数错误'))
        # 判断支付方式是否存在
        try:
            payment = Payment.objects.get(pk=payment)
        except:
            return JsonResponse(json_msg(2, '支付方式暂未开通'))
        # 判断订单是否存在
        try:
            order = Order.objects.get(order_sn=order_sn, user_id=user_id)
        except:
            return JsonResponse(json_msg(3, '订单编号不正确'))
        alipay = alipayfun()
        if payment.name == '支付宝':
            # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
            order_string = alipay.api_alipay_trade_wap_pay(
                out_trade_no=order_sn,
                total_amount=str(order.order_price),
                subject='超市购物订单',  # 订单描述
                return_url="http://127.0.0.1:8000/orderform/completionfpayment/",
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            # 拼接url
            url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
            return JsonResponse(json_msg(0, '成功', data=url))


# 支付成功后展示页面以及修改订单状态
class AlterOrderStatus(View):
    def get(self, request):
        alipay = alipayfun()
        # 获取订单编号
        order_sn = request.GET.get('out_trade_no')
        total_amount = request.GET.get('total_amount')
        # check order status
        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break

            # 继续执行
            # check every 3s, and 10 times in all
            sleep(3)
            print("not paid...")

        # 判断支付是否成功
        context = {
            'order_sn': order_sn,
            'total_amount': total_amount,
        }
        if paid is False:
            # 支付失败
            context['result'] = "支付失败"
        else:
            # 支付成功
            context['result'] = "支付成功"
        return render(request, 'orderform/completionofpayment.html', context=context)

    def post(self, request):
        alipay = alipayfun()
        # 获取订单编号
        order_sn = request.POST.get('out_trade_no')
        order = Order.objects.get(order_sn=order_sn)
        # check order status
        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break

            # 继续执行
            # check every 3s, and 10 times in all
            sleep(3)
            print("not paid...")

        # 判断支付是否成功
        # 修改订单状态
        if paid is True:
            # 支付成功
            order.order_status = 1
            order.save()
        return HttpResponse('success')


# 修改默认收获地址
class AlterIsDefaultClassView(VerifyLoginView):
    def post(self, request):
        button_id = request.POST.get('button_id')
        try:
            AddressTable2.objects.get(pk=button_id)
            AddressTable2.objects.update(is_default=False)
            AddressTable2.objects.filter(pk=button_id).update(is_default=True)
            return JsonResponse(json_msg(0, '修改成功'))
        except AddressTable2.DoesNotExist:
            return JsonResponse(json_msg(1, '不存在该收获地址'))


# 添加收获地址
class AddAddress(VerifyLoginView):
    def get(self, request):
        old_url = request.META.get('HTTP_REFERER', None)
        if old_url:
            request.session['referer'] = old_url
        return render(request, 'orderform/address.html')

    def post(self, request):
        data = request.POST
        form = CheckAddressModelForm3(data)
        if form.is_valid():
            if form.checkMax(request):
                address = form.save(commit=False)
                user = UserTable.objects.get(pk=int(request.session.get('ID')))
                AddressTable2.objects.filter(is_default=True).update(is_default=False)
                address.user = user
                address.save()
                old_url = request.session.get('referer')
                if old_url:
                    del request.session['referer']
                    return JsonResponse(json_msg(0, '添加成功', old_url))
                else:
                    return render(request, 'orderform/gladdress.html')
            else:
                return JsonResponse(json_msg(1, '数据不合法', data=form.errors))
        else:
            return JsonResponse(json_msg(1, '数据不合法', data=form.errors))
