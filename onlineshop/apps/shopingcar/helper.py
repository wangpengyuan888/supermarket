

from django_redis import get_redis_connection

# 封装ajax消息
# code:0 正确
# code：其他错误
def json_msg(code, msg=None, data=None):

    return {'code': code, 'errmsg': msg, 'data': data}


def get_cart_count(request):
    """获取当前用户购物车中的总数量"""
    user_id = request.session.get('ID')
    if user_id is None:
        return 0
    else:
        # 创建redis连接
        r = get_redis_connection()
        #准备查询的建
        cart_key = f"cart_{user_id}"
        # 获取数据
        values = r.hvals(cart_key)
        # 遍历得到总数量
        total_count = 0
        for v in values:
            total_count += int(v)
        return total_count
