from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

@login_required()
def index(request) :
    print(request.user)
    if request.user.has_perm('api.add_event') :
        print("User can change/add events")
        createEventPermission = True
    else :
        createEventPermission = False
    context = {
        'createEventPermission' : createEventPermission
    }
    print(context)
    return  render(request,'webview/index.html',context)


@api_view(["GET"])
def createEvent(request) :
    #Function to render create template page
    return render(request, '')