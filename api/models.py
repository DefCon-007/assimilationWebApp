from django.db import models

class event(models.Model) :
    title = models.CharField(max_length=250)
    description = models.TextField()
    # creator = models.FOr
    helpers = models.TextField()
class attendanceTakers(models.Model) :
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
class student(models.Model) :
    name = models.CharField(max_length=250)
    rollno = models.CharField(max_length=20)
    email = models.CharField(max_length=250)
# Create your models here.
