from django.contrib.auth.models import User,Group
from django.db import models

class event(models.Model) :
    title = models.CharField(max_length=250)
    description = models.TextField()
    venue = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    audience = models.ManyToManyField(Group, related_name="group_events")
    # creator = models.FOr
    helpers = models.ManyToManyField(User, related_name="manytomanyevents")
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="owned_events")
class attendance(models.Model) :
    event = models.ForeignKey(event, on_delete=models.PROTECT,default=None,related_name="eventName")
    user = models.ForeignKey(User, on_delete=models.PROTECT,default=None,related_name="student")
    attendanceStatus = models.NullBooleanField(null=True,blank=True)
class student(models.Model) :
    name = models.CharField(max_length=250)
    rollno = models.CharField(max_length=20)
    email = models.CharField(max_length=250)
# Create your models here.
