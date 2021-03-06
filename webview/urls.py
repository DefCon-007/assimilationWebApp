from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createevent', views.createEvent, name='createevent'),
    path('upcomingevents', views.upcomingEvents, name="upcomingevents"),
    path('markattendance', views.markAttendance, name="markattendance"),
    path('editevent', views.editevent, name="editevent"),
    path('complaint', views.complaint, name = 'complaint'),
    path('allcomplaints', views.allComplaints, name="allComplaints"),
    path('changeComplaintStatus', views.changeComplaintStatus, name="changeComplaintStatus"),
    path('changepassword',views.changePassword, name="changepassword"),
    path('deleteevent', views.deleteEvent, name="deleteevent")
        ]