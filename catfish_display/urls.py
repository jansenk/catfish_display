from django.conf.urls import patterns, include, url
from desktop import views as desktopViews

urlpatterns = patterns('',
    url(r'^call/(.*?)/', desktopViews.call, name="call"),
    url(r'^location/(.*?)/', desktopViews.tracerouteLocation, name="location"),
	url(r'^desktop/mtr/(.*?)/', desktopViews.desktopMtrDisplay, name="mtr"),
    url(r'^desktop/(.*?)/', desktopViews.desktopCall, name="desktopCall"),
    url(r'^desktop/', desktopViews.desktop, name="desktop"),
    url(r'^server/graph/(.*?)/', desktopViews.callServerGraph, name="serverGraph"),
    url(r'^server/', desktopViews.server, name="server"),
    url(r'^dagre/', desktopViews.dag),
    url(r'^$', desktopViews.index, name="index"),
)



