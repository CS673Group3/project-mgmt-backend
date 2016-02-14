from django.conf.urls import patterns, url, include
from comm import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
