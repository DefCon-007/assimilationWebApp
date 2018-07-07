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
    helpers = models.ManyToManyField(User, related_name="manytomanyevents", blank=True, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="owned_events")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
class attendance(models.Model) :
    event = models.ForeignKey(event, on_delete=models.PROTECT,default=None,related_name="eventName")
    user = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="student")
    attendanceStatus = models.NullBooleanField(null=True,blank=True)
class student(models.Model) :
    name = models.CharField(max_length=250)
    rollno = models.CharField(max_length=20)
    email = models.CharField(max_length=250)

class complaint(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField(blank=True,null=True)
    event = models.ForeignKey(event, on_delete=models.PROTECT,default=None,related_name="complaintEvent")
    user = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="complaintUser")
    resolutionStatus = models.BooleanField(default=False)
    createdDateTime = models.DateTimeField(blank=True, null=True)
# Create your models here.
