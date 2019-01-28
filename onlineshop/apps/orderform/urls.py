from django.conf.urls import url

from orderform import views

urlpatterns = [
    url(r'^sureorder', views.SureOrder.as_view(), name='sureorder'),
    url(r'^addaddress', views.AddAddress.as_view(), name='addaddress'),
]