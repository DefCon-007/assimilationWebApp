from django.urls import path,include

from . import views

urlpatterns = [
    path('login', views.login),
    path('createevent', views.createEvent),
    path('upcomingevent', views.upcomingevent),
    path('singlestudentattendance',views.markSingleUserAttendance),
    path('getstudentattendancelist', views.getStudentAttendanceList),
    path('changepassword', views.changePassword),
    path('deleteevent', views.deleteEvent),
        ]