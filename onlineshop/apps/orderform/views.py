from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from db.Base_View import VerifyLoginView
from orderform.forms import CheckAddressModelForm3
from orderform.models import AddressTable2
from shopingcar.helper import json_msg

from user.models import UserTable
# 所有订单页面
class AllOrderClassView(VerifyLoginView):
    def get(self, request):
        return render(request, 'orderform/allorder.html')

# 确认订单
class SureOrder(VerifyLoginView):
    def get(self, request):
        user_id = request.session.get("ID")
        data = AddressTable2.objects.filter(user_id=user_id).order_by('-is_default')
        return render(request, 'orderform/tureorder.html', {'data': data})

    def post(self, request):
        pass

# 管理收获地址
class AdminAddressClassView(VerifyLoginView):
    def get(self, request):
        user_id = request.session.get('ID')
        data = AddressTable2.objects.filter(user_id=user_id).order_by('-is_default')
        return render(request, 'orderform/gladdress.html', {'data': data})

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

