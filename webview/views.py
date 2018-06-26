import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.src import utils
import traceback
from api.src import databaseConnection as db
# Create your views here.
from rest_framework.decorators import api_view
from assimilation import settings
@login_required()
def index(request) :
    print(request.user)
    if request.user.has_perm('api.add_event') :
        print("User can change/add events")
        createEventPermission = True
    else :
        createEventPermission = False
    grpList = list()
    for g in request.user.groups.all():
        try :
            grpList.append(settings.GROUPS_MAP[g.name])
        except :
            print(f"Exception for {g.name}")
    context = {
        'createEventPermission' : createEventPermission,
        'grpList' : grpList
    }


    return  render(request,'webview/index.html',context)


@api_view(["GET","POST"])
@login_required()
def createEvent(request) :
    if request.user.has_perm('api.add_event'):
        if request.method == "POST" :
            data = request.data
            try :
                title = data["title"][0]
                description = data["description"][0]
                venue = data["venue"][0]
                date=data["date"][0]
                time = data["time"][0]
                audience = data["audience"]

            except Exception as e :
                print(f"webview:createEvent:Following exeception occured.\n{e}\n{traceback.format_exc()}")

        else :
            grpNameList = list()
            grpNameMapped = list()
            for g in request.user.groups.all():
                grpNameList.append(g.name)
                try :
                    grpNameMapped.append({
                        "value" : settings.GROUPS_MAP[g.name],
                        "key" : g.name
                    })
                except :
                    print(f"Exception for {g.name}")
            validHelpersList = db.getHelpersFromGroupName(grpNameList)
            helperListForView = list()
            for helper in validHelpersList :
                helperListForView.append({
                    "username" : helper.username,
                    "fullname" : helper.get_full_name()
                })
            #Function to render create template page
            context={"mindate":datetime.datetime.today().strftime('%Y-%m-%d'),
                     "createEventPermission":True,
                     "helpers" : helperListForView,
                     "audience" : grpNameMapped,
                     }

            return render(request, 'webview/createevent.html', context=context)
    else :
        return render(request, 'webview/errorPage.html', {
            "d1" : 4, "d2" : 0 , "d3" : 1, "msg" : "Sorry! You are not authorized for this."
        })