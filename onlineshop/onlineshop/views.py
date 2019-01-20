from django.shortcuts import render
from django.views import View


class MainClassView(View):
    def get(self, request):
        return render(request, 'mainitem/index.html')