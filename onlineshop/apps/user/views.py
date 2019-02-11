import random
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from db.Base_View import VerifyLoginView
from django.views import View
from user.forms import RegisterModelForm, LoginModelForm, AlterInfoModelForm, AlterPassWordModelForm, PassWordForm
from user.helper import set_pwd, send_sms, login
from user.models import UserTable

# 登陆页面
class LoginClassView(View):
    def get(self, request):
        return render(request, 'user/login.html')


    # 对表单提交的数据进行保存
    def post(self, request):
        data = request.POST
        # 数据进行合法性验证
        form = LoginModelForm(data)
        if form.is_valid():
            # 如果数据合法
            user = form.cleaned_data.get('user')
            # 设置session
            # request.session['ID'] = user.pk
            # request.session['user_name'] = user.user_name
            # request.session['head'] = user.head
            # request.session.set_expiry(9999)  # 9999秒后就消失
            login(request, user)
            referer = request.session.get('referer')
            if referer:
                del request.session['referer']
                return redirect(referer)
            else:
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
        return render(request, 'user/reg.html')

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
            return render(request, 'user/reg.html', context=context)


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
        head = request.FILES.get('head')
        item = UserTable.objects.get(pk=request.session.get('ID'))
        form = AlterInfoModelForm(data, instance=item)
        if form.is_valid():
            # 数据合法
            # 存储数据库
            form.save()
            user = UserTable.objects.get(pk = request.session.get('ID'))
            if head is not None:
                user.head = head
            user.save()
            login(request, user)


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
        data = request.POST
        form = AlterPassWordModelForm(data)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            pass_word = set_pwd(form.cleaned_data.get('pass_word'))
            UserTable.objects.filter(user_name=user_name).update(pass_word=pass_word)
            return redirect('user:login')
        else:
            context = {
                'errors': form.errors,
                'data': data
            }
            return render(request, 'user/forgetpassword.html', context=context )


# 安全设置
class SecuritySettings(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/saftystep.html')


# 修改密码
class PassWordClassView(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/password.html')

    def post(self, request):
        data = request.POST
        form = PassWordForm(data)
        if form.is_valid():
            if form.checkPassword(request):
                UserTable.objects.filter(pk=request.session.get('ID')).update(pass_word=set_pwd(form.cleaned_data.get('new_pass_word')))
                return redirect('user:securitysettings')
            else:
                return render(request, 'user/password.html', {'errors': form.errors})
        else:
            context = {
                'data': data,
                'errors': form.errors
            }
            return render(request, 'user/password.html', context=context)


# 发送验证码信息
class SendMsg(View):
    def get(self, request):
        pass

    def post(self, request):
        user_name = request.POST.get('user_name', '')
        # 验证数据的合法性
        rs = re.search('^1[3-9]\d{9}$', user_name)
        if rs is None:
            return JsonResponse({'error': 1, 'errmsg': '电话号码格式错误!'})

        # 生成随机验证码
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        print("=============随机验证码为==={}==============".format(random_code))

        # >>>2. 保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(user_name, random_code)
        r.expire(user_name, 60)  # 设置60秒后过期

        # 首先获取当前手机号码的发送次数
        key_times = "{}_times".format(user_name)
        now_times = r.get(key_times)  # 从redis获取的二进制,需要转换
        # print(int(now_times))
        if now_times is None or int(now_times) < 5:
            # 保存手机发送验证码的次数, 不能超过5次
            r.incr(key_times)
            # 设置一个过期时间
            r.expire(key_times, 3600)  # 一个小时后再发送
        else:
            # 返回,告知用户发送次数过多
            return JsonResponse({"error": 1, "errmsg": "发送次数过多"})

        # >>>3. 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"你好---阿斌\"}" % random_code
        # print(params)
        rs = send_sms(__business_id, user_name, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        # 3. 合成响应
        return JsonResponse({'error': 0})