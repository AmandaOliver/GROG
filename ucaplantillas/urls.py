from django.conf.urls import patterns, url

from ucaplantillas import views

urlpatterns = patterns('',
                       url(r'^$', views.ejemplo, name='ejemplo'),
)
