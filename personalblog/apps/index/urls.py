from django.conf.urls import url

from apps.index import views

urlpatterns = [

    url(r'^$', views.Index.as_view(), name='首页'),

]
