from django.shortcuts import render
from django.views import View

# 主页面
class MainClassView(View):
    def get(self, request):
        return render(request, 'goods/index.html')

    def post(self, request):
        pass


# 详情页
class DetailClassView(View):
    def get(self, request):
        return render(request, 'goods/detail.html')

    def post(self, request):
        pass


class CategoryClassView(View):
    def get(self, request):
        return render(request, 'goods/category.html')

    def post(self, request):
        pass