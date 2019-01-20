import hashlib


# 加密密码
def set_pwd(pwd):
    for _ in range(6666):
        pwd = '{}{}'.format(pwd, '6666')
        new_pwd = hashlib.md5(pwd.encode('utf-8'))
    return new_pwd