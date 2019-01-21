from django.http import HttpResponse
from django.shortcuts import render, redirect
from db.Base_View import VerifyLoginView
from django.views import View
from user.forms import RegisterModelForm, LoginModelForm, AlterInfoModelForm
from user.helper import set_pwd
from user.models import UserTable

# 登陆页面
class LoginClassView(View):
    def get(self, request):
        return render(request, 'user/templates/user/login.html')


    # 对表单提交的数据进行保存
    def post(self, request):
        data = request.POST
        # 数据进行合法性验证
        form = LoginModelForm(data)
        if form.is_valid():
            # 如果数据合法
            user = form.cleaned_data.get('user')
            # 设置session
            request.session['ID'] = user.pk
            request.session['user_name'] = user.user_name
            # request.session['head'] = user.head
            request.session.set_expiry(9999)  # 关闭浏览器就消失
            return redirect('user:member')
        else:
            # 数据不合法 回显网页
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


# 个人中心
class MemberClassView(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/member.html')


# 修改个人信息
class PersonInfoClassView(VerifyLoginView):
    def get(self, request):
        data = UserTable.objects.get(pk=request.session.get('ID'))
        return render(request, 'user/infor.html', {'data': data})

    def post(self, request):
        data = request.POST
        item = UserTable.objects.get(pk=request.session.get('ID'))
        form = AlterInfoModelForm(data, instance=item)
        if form.is_valid():
            # 数据合法
            # 存储数据库
            form.save()
            return redirect('user:info')
        else:
            context = {
                'errors': form.errors,
                'data': data
            }
            return render(request, 'user/infor.html', context=context)


# 忘记密码
class ForgetPwdClassView(View):
    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        pass