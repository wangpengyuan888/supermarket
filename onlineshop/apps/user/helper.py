import hashlib


# 加密密码
def set_pwd(pwd):
    for _ in range(6666):
        pwd_str = '{}{}'.format(pwd, '6666')
        h= hashlib.md5(pwd_str.encode('utf-8'))
        pwd = h.hexdigest()
    return pwd