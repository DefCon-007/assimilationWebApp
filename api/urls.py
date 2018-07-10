from django.urls import path,include

from . import views

urlpatterns = [
    path('login', views.login),
    path('createevent', views.createEvent)
        ]