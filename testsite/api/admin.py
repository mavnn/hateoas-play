from django.contrib import admin

from .models import Timeline, TimelineEvent

admin.site.register([Timeline, TimelineEvent])
