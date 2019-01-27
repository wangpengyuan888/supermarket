import hashlib
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from django.http import JsonResponse

from django.shortcuts import redirect, render

# 加密密码
from onlineshop.settings import ACCESS_KEY_ID, ACCESS_KEY_SECRET
from shopingcar.helper import json_msg


def set_pwd(pwd):
    for _ in range(6666):
        pwd_str = '{}{}'.format(pwd, '6666')
        h= hashlib.md5(pwd_str.encode('utf-8'))
        pwd = h.hexdigest()
    return pwd

# 检查登陆状态
def check_login(func):
    def verify_login(request, *args, **kwargs):
        if request.session.get('ID') is None:
            # 将上一次请求的地址存入session
            referer = request.META.get('HTTP_REFERER', None)
            if referer:
                request.session['referer'] = referer
            if request.is_ajax():
                return JsonResponse(json_msg(1, '账号为未登陆'))
            else:
                return redirect('user:login')
        else:
            return func(request, *args, **kwargs)
    return verify_login


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

# 发送信息
def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


def login(request,user):#保存session的方法
    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    request.session['head'] = user.head
    request.session.set_expiry(0)  # 关闭浏览器就消失
