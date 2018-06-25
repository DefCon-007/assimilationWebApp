from django.contrib import admin
from .models import  *

modelList = [attendanceTakers,student,event]
admin.site.register(modelList)

# Register your models here.
