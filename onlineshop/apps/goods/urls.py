from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^main/$', views.MainClassView.as_view(), name='main'),
    url(r'^detail/(.*?)$', views.DetailClassView.as_view(), name='detail'),
    url(r'^category/$', views.CategoryClassView.as_view(), name='category'),
]