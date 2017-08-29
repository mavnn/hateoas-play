from django.db import models
import uuid

class Timeline(models.Model):
    title = models.CharField(max_length=240)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title

    class meta:
        ordering = ('title',)

class TimelineEvent(models.Model):
    title = models.CharField(max_length=240)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateField()
    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timelines = models.ManyToManyField(Timeline)

    def __str__(self):
        return self.title

    class meta:
        ordering = ('date',)
