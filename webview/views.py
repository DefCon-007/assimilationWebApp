from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.src import utils
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
@login_required()
def createEvent(request) :
    return render(request, 'webview/errorPage.html', {
        "d1": 4, "d2": 0, "d3": 4
    })
    if request.user.has_perm('api.add_event'):
        dataForm = utils.eventForm
        #Function to render create template page
        return render(request, 'webview/createevent.html', {'form':dataForm, })
    else :
        return render(request, 'webview/errorPage.html', {
            "d1" : 4, "d2" : 0 , "d3" : 4
        })