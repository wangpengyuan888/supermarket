from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.forms import RegisterModelForm, LoginModelForm
from user.helper import set_pwd
from user.models import UserTable

# 登陆页面
class LoginClassView(View):
    def get(self, request):
        return render(request, 'user/templates/user/login.html')



    def post(self, request):
        data = request.POST
        form = LoginModelForm(data)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            request.session['ID'] = user.pk
            request.session['phone'] = user.phone
            # request.session['head'] = user.head
            request.session.set_expiry(0)  # 关闭浏览器就消失
            return redirect('user:member')
        else:
            context ={
                'data': form.errors
            }
            return render(request, 'user/login.html', context=context)



# 注册页面
class RegisterClassView(View):
    # 请求为get的时候进入注册表单页面
    def get(self, request):
        return render(request, 'user/templates/user/reg.html')

    # 请求为post将表单提交的数据保存
    def post(self, request):
        data = request.POST
        form = RegisterModelForm(data)
        if form.is_valid():
            # 数据合法进行保存
            user_name = form.cleaned_data.get('user_name')
            pass_word = set_pwd(form.cleaned_data.get('pass_word'))
            UserTable.objects.create(user_name=user_name, pass_word=pass_word)
            # 跳转到登陆页面
            return redirect('user:login')
        else:
            # 数据不合法，回显页面
            context = {
                'data': data,
                'errors': form.errors
            }
            return render(request, 'user/templates/user/reg.html', context=context)



class MemberClassView(View):
    def get(self, request):
        if request.session.get("ID") is None:
            return redirect('user:login')
        else:
            return render(request, 'user/member.html')

