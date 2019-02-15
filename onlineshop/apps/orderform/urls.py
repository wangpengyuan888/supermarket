from django.conf.urls import url

from orderform import views

urlpatterns = [
    url(r'^sureorder/$', views.SureOrder.as_view(), name='sureorder'),
    url(r'^addaddress/$', views.AddAddress.as_view(), name='addaddress'),
    url(r'^allorder/$', views.AllOrderClassView.as_view(), name='allorder'),
    url(r'^adminaddress/$', views.AdminAddressClassView.as_view(), name='adminaddress'),
    url(r'^alterisdefault/$', views.AlterIsDefaultClassView.as_view(), name='alterisdefault'),
    url(r'^ordersave/$', views.OrderSave.as_view(), name='Ordersave'),
    url(r'^surepay/$', views.SurePay.as_view(), name='surepay'),
    url(r'^completionfpayment/$', views.AlterOrderStatus.as_view(), name='completionfpayment'),
]