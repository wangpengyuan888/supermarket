from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class LoginClassView(View):
    def get(self, request):
        return render(request, 'useritem/login.html')

    def post(self, request):
        return HttpResponse('ok')


class RegisterClassView(View):
    def get(self, request):
        return render(request, 'useritem/reg.html')

    def post(self, request):
        return HttpResponse('ok')