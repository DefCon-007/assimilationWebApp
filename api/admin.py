from django.contrib import admin
from .models import  *

modelList = [attendance,student, complaint]
admin.site.register(modelList)

class EventList(admin.ModelAdmin) :
    filter_horizontal = ['helpers']

admin.site.register(event,EventList)
# Register your models here.
