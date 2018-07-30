from django.contrib import admin
from .models import  *

# modelList = []
# admin.site.register(modelList)
# #
# class EventList(admin.ModelAdmin) :
#
#

# Register your models here.

#
#
# class EmailExtractTempelateResource(resources.ModelResource):
#     class Meta:
#         model = EmailExtractTempelate


# class EmailExtractTempelateAdmin(ImportExportMixin, admin.ModelAdmin):
#     resource_class = EmailExtractTempelateResource
#     list_filter = ["query"]
#     list_display = []
#     for columnName in EmailExtractTempelate._meta.fields :
#         list_display.append(columnName.get_attname_column()[0])
#     list_display.remove("emailhtml")
# # Register your models here.
# class EmailExtractDataResource(resources.ModelResource):
#     class Meta:
#         model = EmailExtractedData
class attendanceAdmin(admin.ModelAdmin) :
    list_display = []
    list_filter = ["attendanceStatus","event"]
    for columnName in attendance._meta.fields :
        list_display.append(columnName.get_attname_column()[0])

admin.site.register(attendance,attendanceAdmin)


class eventAdmin(admin.ModelAdmin) :
    list_display = []
    list_filter = ["datetime","audience","title"]
    filter_horizontal = ['helpers']
    for columnName in event._meta.fields :
        list_display.append(columnName.get_attname_column()[0])

admin.site.register(event,eventAdmin)


class complaintAdmin(admin.ModelAdmin) :
    list_display = []
    list_filter = ["createdDateTime","event","resolutionStatus"]
    for columnName in complaint._meta.fields :
        list_display.append(columnName.get_attname_column()[0])


class UserDeviceAdmin(admin.ModelAdmin) :
    list_display = []
    for columnName in UserDeviceIdAndAuthToken._meta.fields :
        list_display.append(columnName.get_attname_column()[0])
admin.site.register(UserDeviceIdAndAuthToken,UserDeviceAdmin)