from django.shortcuts import render
from django.views import View

# 主页面
from goods.models import GoodsSPU, GoodsSKU, GoodsCategory


class MainClassView(View):
    def get(self, request):
        return render(request, 'goods/index.html')

    def post(self, request):
        pass


# 详情页
class DetailClassView(View):
    def get(self, request, good_id):
        data = GoodsSKU.objects.get(pk=good_id)
        return render(request, 'goods/detail.html', {'data': data})

    def post(self, request, good_id):
        pass

# 商品分类页
class CategoryClassView(View):
    # 1.
    # 页面刚加载的时候
    # 显示的商品只
    # 显示
    # 排序
    # 排第一的分类下的商品
    # 2.
    # 点击哪个分类
    # 就显示
    # 对应分类下的商品
    # 3.
    # 可以按照
    # 销量, 价格(降, 升), 添加时间, 综合(pk)
    # 排序
    # 并且
    # 是对应分类下的商品
    def get(self, request, sort_id, order):
        # 查询出所有的分类
        sort = GoodsCategory.objects.all()
        if sort_id == '':
            # 如果不传默认给第一个
            category = sort.first()
            sort_id = category.pk
        else:
            # 前端页面的样式需要比较判断，所以转成字符串
            sort_id = int(sort_id)
            # 得到对应分类id的对象
            category = GoodsCategory.objects.get(pk=sort_id)

        # 查询出对应分类的商品信息
        data = GoodsSKU.objects.filter(is_selling=True, goods_category=category)
        # 分别按照id，销量，价格升序，价格降序，添加时间进行排序
        order_rule = ['pk', '-sales', 'price', '-price', '-create_time']
        # 什么都不传的时候默认按照id排序
        if order == '':
            order = 0
        order = int(order)
        data = data.order_by(order_rule[order])

        context = {
            'data': data,
            'sort': sort,
            'sort_id': sort_id,
            'order': order
        }
        return render(request, 'goods/category.html', context=context)

    def post(self, request, sort_id):
        pass