from django.conf.urls import url
from shopingcar import views

urlpatterns = [
    url(r'^addcar/$', views.AddCarClassView.as_view(), name='addcar'),
    url(r'^reducecar/$', views.ReduceCarClassView.as_view(), name='reducecar'),
    url(r'^cart/$', views.CartClassView.as_view(), name='cart'),
]