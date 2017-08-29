from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import Timeline
import json
import iso8601
import uuid

def asJson(func):
    def wrapped(*args, **kwargs):
        responseData = func(*args, **kwargs)
        if 'error' in responseData and 'error_code' in responseData:
            status = responseData['error_code']
        else:
            status = 200
        content_type = 'application/json'
        content = json.dumps(responseData)
        resp = HttpResponse(content=content, content_type=content_type, status=status)
        resp['Content-Length'] = len(content)
        resp['status_code'] = status
        return resp
    return wrapped

def authed(func):
    def protected(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return { 'error' : 'You must log in to use this api',
                     'error_code': 403,
                     'links': [{'rel':'login',
                                'href':'/api/login'}] }
    return protected

@asJson
@authed
def index(request):
    return {
        'user': {
            'name': request.user.username,
            'email': request.user.email,
        },
        'links' : [
            {
                'rel': 'self',
                'href': '/api/'
            },
            {
                'rel': 'timeline.list',
                'href': '/api/timelines'
            },
            {   'rel': 'timeline.add',
                'href': '/api/timelines'
            },
            {
                'rel': 'timelineEvents.list',
                'href': '/api/timelineEvents'
            },
            {
                'rel': 'logout',
                'href': '/api/logout'
            }
        ]
    }

def loginView(request):
    post_data = json.loads(request.body.decode('utf-8'))
    user = authenticate(request, username=post_data['username'], password=post_data['password'])
    if user is not None:
        login(request, user)
        return index(request)
    else:
        @asJson
        def j ():
            return { 'error': 'Invalid credentials',
                     'error_code': 403,
                     'links': [{'rel':'login',
                                'href':'/api/login'}] }
        return j()

def timelineSummary(t):
    return { 'title': t.title,
             'links': [{'rel':'self','href':'/api/timeline/' + str(t.eid) },
                       {'rel':'timelineEvent.add','href':'/api/timelineEvents/' + str(t.eid) }]}

def timelineDetail(t):
    return { 'title': t.title,
             'links': [{'rel':'self','href':'/api/timeline/' + str(t.eid) }] +
                      [{'rel':'timelineEvent','href':'/api/timelineEvent/' + str(te.eid)} for te in t.timelineevent_set.all() ] +
                      [{'rel':'timelineEvent.add','href':'/api/timelineEvents/' + str(t.eid) }]}

def getTimelines(request):
    timelines = request.user.timeline_set.all()
    return [timelineSummary(t) for t in timelines]

def postTimelines(request):
    title = request.body.decode('utf-8')
    timeline = request.user.timeline_set.create(title=title)
    timeline.save()
    return getTimelines(request)

@asJson
@authed
def timelines(request):
    if request.method == 'GET':
        return getTimelines(request)
    elif request.method == 'POST':
        return postTimelines(request)

@asJson
@authed
def timeline(request, timeline_id):
    t = request.user.timeline_set.get(eid=uuid.UUID(timeline_id))
    return timelineDetail(t)

def timelineEventSummary(te):
    return { 'title': te.title,
             'date': te.date.isoformat(),
             'links': [{'rel':'self', 'href':'/api/timelineEvent/' + str(te.eid)}] }

def timelineEventDetails(te):
    return { 'title': te.title,
             'date': te.date.isoformat(),
             'links': [{'rel':'self', 'href':'/api/timelineEvent/' + str(te.eid)}] +
                      [{'rel':'timeline', 'href':'/api/timeline/' + str(t.eid)} for t in te.timelines.all() ]}

@asJson
@authed
def timelineEvents(request):
    timelineEvents = request.user.timelineevent_set.all()
    return [timelineEventSummary(te) for te in timelineEvents]

def addTimelineEvent(request, timeline_id):
    post_data = json.loads(request.body.decode('utf-8'))
    timeline = request.user.timeline_set.get(eid=uuid.UUID(timeline_id))
    te = timeline.timelineevent_set.create(title=post_data['title'], date=iso8601.parse_date(post_data['date']), owner_id=request.user.id)
    te.save()
    return timelineEvent(request, str(te.eid))

@asJson
@authed
def timelineEvent(request, timelineEvent_id):
    timelineEvent = request.user.timelineevent_set.get(eid=uuid.UUID(timelineEvent_id))
    return timelineEventDetails(timelineEvent)
