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
    def get(self, request):
        sort = GoodsCategory.objects.all()
        data = GoodsSKU.objects.all()
        context = {
            'data': data,
            'sort': sort
        }
        return render(request, 'goods/category.html', context=context)

    def post(self, request):
        pass