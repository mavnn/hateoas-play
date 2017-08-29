from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^timelines$', csrf_exempt(views.timelines), name='timelines'),
    url(r'^timeline/(?P<timeline_id>.+)$', views.timeline, name='timeline'),
    url(r'^timelineEvents$', views.timelineEvents, name='timelineEvents'),
    url(r'^timelineEvents/(?P<timeline_id>.+)$', csrf_exempt(views.addTimelineEvent), name='addTimelineEvent'),
    url(r'^timelineEvent/(?P<timelineEvent_id>.+)$', views.timelineEvent, name='timelineEvent'),
    url(r'^login$', csrf_exempt(views.loginView), name='login')
]
