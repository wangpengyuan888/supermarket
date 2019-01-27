from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from db.Base_View import VerifyLoginView

from django_redis import get_redis_connection
from goods.models import GoodsSKU
from shopingcar.helper import json_msg, get_cart_count


# 操作购物车，添加数据
class AddCarClassView(VerifyLoginView):
    def get(self, request):
        return HttpResponse('ok')

    def post(self, request):
        """
        需要接受的参数
        用户id
        商品id
        商品数量
        :param request:
        :return:
        """
        # 接受参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        good_count = request.POST.get('good_count')
        try:
            #1. 判断是否为整数
            sku_id = int(sku_id)
            good_count = int(good_count)
        except:
            return JsonResponse(json_msg(2, '参数错误'))
        # 2.要在数据库中存在商品
        try:
            good_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(3, '商品不存在'))
        # 判断库存
        if good_sku.stock < good_count:
            return JsonResponse(json_msg(4, '库存不足'))

        # 操作数据库
        # 创建链接
        r = get_redis_connection()
        # 处理购物车的key
        cart_key = f'cart_{user_id}'
        # 添加
        # 获取购物车已经存在的数量， 加上要添加的和库存进行比较
        old_count = r.hget(cart_key, sku_id)
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)
        if old_count+good_count > good_sku.stock:
            return JsonResponse(json_msg(3, '库存不足'))
        # 将商品添加到购物车
        r.hincrby(cart_key, sku_id, good_count)
        # 获取购物车中的总数量
        cart_count = get_cart_count(request)
        return JsonResponse(json_msg(0, '添加购物车成功', data=cart_count))

# 操作购物车，减少数据
class ReduceCarClassView(VerifyLoginView):
    def get(self, request):
        return HttpResponse('ok')

    def post(self, request):
        """
        需要接受的参数
        用户id
        商品id
        商品数量
        :param request:
        :return:
        """
        # 接受参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        good_count = request.POST.get('good_count')
        try:
            #1. 判断是否为整数
            sku_id = int(sku_id)
            good_count = int(good_count)
        except:
            return JsonResponse(json_msg(2, '参数错误'))
        # 2.要在数据库中存在商品
        try:
            good_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(3, '商品不存在'))
        # 判断库存
        if good_sku.stock < good_count:
            return JsonResponse(json_msg(4, '库存不足'))

        # 操作数据库
        # 创建链接
        r = get_redis_connection()
        # 处理购物车的key
        cart_key = f'cart_{user_id}'
        # 添加
        # 获取购物车已经存在的数量， 加上要添加的和库存进行比较
        old_count = r.hget(cart_key, sku_id)
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)
        if old_count+good_count > good_sku.stock:
            return JsonResponse(json_msg(3, '库存不足'))
        # 将商品添加到购物车
        r.hincrby(cart_key, sku_id, -good_count)
        # 获取购物车中的总数量
        cart_count = get_cart_count(request)
        return JsonResponse(json_msg(0, '添加购物车成功', data=cart_count))


# 购物车页面
class CartClassView(VerifyLoginView):
    def get(self, request):
        return render(request, 'shopingcar/shopcart.html')
    def post(self, request):
        pass