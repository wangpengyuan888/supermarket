from django.conf.urls import url

from apps.user import views

urlpatterns = [
    url(r'^login/$', views.LoginClassView.as_view(), name='login'),
    url(r'^register/$', views.RegisterClassView.as_view(), name='register'),
    url(r'member/$', views.MemberClassView.as_view(), name='member'),

]