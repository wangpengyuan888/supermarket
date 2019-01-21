import hashlib


# 加密密码
from django.shortcuts import redirect, render


def set_pwd(pwd):
    for _ in range(6666):
        pwd_str = '{}{}'.format(pwd, '6666')
        h= hashlib.md5(pwd_str.encode('utf-8'))
        pwd = h.hexdigest()
    return pwd


def check_login(func):
    def verify_login(request, *args, **kwargs):
        if request.session.get('ID') is None:
            return redirect('user:login')
        else:
            return func(request, *args, **kwargs)
    return verify_login