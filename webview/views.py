from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

@api_view(["get"])
def index(request) :
    print(request.user)
    return  render(request,'./registration/login.html')


@api_view(["GET"])
def createEvent(request) :
    #Function to render create template page
    return render(request, '')