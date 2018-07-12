from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^flush/$', views.flush, name='mysite_flush'),
    url(r'^form_input/$', views.form_input, name='form_input'),
]
