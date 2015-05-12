from django.conf.urls import patterns, include, url
from django.contrib import admin
import desktop

urlpatterns = patterns('',
    url(r'^$', include(desktop.urls)),
)
