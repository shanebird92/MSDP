from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^test/$', views.test, name='mysite_test'),
    re_path(r'^flush/$', views.flush, name='mysite_flush'),
]
