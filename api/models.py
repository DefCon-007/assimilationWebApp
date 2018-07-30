from django.contrib.auth.models import User,Group
from django.db import models
import uuid
class event(models.Model) :
    title = models.CharField(max_length=250)
    description = models.TextField()
    venue = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    audience = models.ManyToManyField(Group, related_name="group_events")
    # creator = models.FOr
    helpers = models.ManyToManyField(User, related_name="manytomanyevents", blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="owned_events")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title

class attendance(models.Model) :
    event = models.ForeignKey(event, on_delete=models.CASCADE,default=None,related_name="eventName")
    user = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="student")
    attendanceStatus = models.NullBooleanField(null=True,blank=True)

class UserDeviceIdAndAuthToken(models.Model) :
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name="authTable")
    token = models.UUIDField(default=uuid.uuid4)
    deviceId = models.CharField(max_length=250, blank=True, null=True)


class complaint(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField(blank=True,null=True)
    event = models.ForeignKey(event, on_delete=models.CASCADE,default=None,related_name="complaintEvent")
    user = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="complaintUser")
    resolutionStatus = models.BooleanField(default=False)
    createdDateTime = models.DateTimeField(blank=True, null=True)
# Create your models here.
