from django.conf.urls import patterns,url
from desktop import views


urlpatterns = patterns("",
                       url(r'^$', views.listCalls, name='index'),
                       )