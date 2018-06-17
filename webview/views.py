from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view


@api_view(["get"])
def index(request) :
    return  render(request,'./registration/login.html')