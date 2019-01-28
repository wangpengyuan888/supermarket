from django.shortcuts import render
from db.Base_View import VerifyLoginView

class SureOrder(VerifyLoginView):
    def get(self, request):
        return render(request, 'orderform/tureorder.html')

    def post(self, request):
        pass


class AddAddress(VerifyLoginView):
    def get(self, request):
        return render(request, 'orderform/address.html')
