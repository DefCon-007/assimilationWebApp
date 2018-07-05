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
    grpList = list()
    for g in request.user.groups.all():
        try :
            grpList.append(settings.GROUPS_MAP[g.name])
        except :
            print(f"Exception for {g.name}")
    context = {

        'grpList' : grpList
    }


    return  render(request,'webview/index.html',context)


@api_view(["GET","POST"])
@login_required()
def createEvent(request) :
    if request.user.has_perm('api.add_event'):
        if request.method == "POST" :
            data = request.data
            print(request.data)
            try :
                title = data["title"]
                description = data["description"]
                venue = data["venue"]
                date=data["date"]
                time = data["time"]
                datetimestring = date + "|"+time
                datetimeobject = datetime.datetime.strptime(datetimestring,"%Y-%m-%d|%H : %M")
                audience = request.POST.getlist('audience')
                helpers = request.POST.getlist('helpers')
                db.addNewEvent(title=title, description=description, venue=venue, datetimeobj=datetimeobject, audiences=audience, helpers=helpers, createdBy=request.user)
                context = {
                    "swal" :{
                        "title" : "Success",
                        "text" : "Event created successfully",
                        "icon" : "success",
                        "butText" : "Close"
                    },
                    "swalFlag" : True,

                }
                return render(request,"webview/createevent.html", context=context)
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
            print(grpNameList)
            validHelpersList = db.getHelpersFromGroupName(grpNameList)
            helperListForView = list()
            for helper in validHelpersList :
                helperListForView.append({
                    "username" : helper.username,
                    "fullname" : helper.get_full_name()
                })
            #Function to render create template page
            context={"mindate":datetime.datetime.today().strftime('%Y-%m-%d'),
                     "helpers" : helperListForView,
                     "audience" : grpNameMapped,
                     }

            return render(request, 'webview/createevent.html', context=context)
    else :
        return render(request, 'webview/errorPage.html', {
            "d1" : 4, "d2" : 0 , "d3" : 1, "msg" : "Sorry! You are not authorized for this."
        })


@api_view(["GET"])
def upcomingEvents(request) :
    print(request.user)
    eventsList = db.getEventFromUsername(request.user.username)
    return render(request, "webview/upcomingevents.html", {"eventsList":eventsList})

@api_view(["GET","POST"])
def markAttendance(request) :
    if request.method == "GET" :
        data = request.query_params
        try :
            eventUUID = data["eventId"]
            event = db.getEventByUUID(eventUUID)
            context = {
                "attendanceList" : db.getAttendanceObjectListFromEvent(event),
                "eventUUID" : eventUUID,
                "eventTitle" : event.title
            }
            return render(request,"webview/markattendance.html",context=context)
        except KeyError:
            return  render(request, "Key error")
    else :
        data = request.data
        try :
            eventUUID = data["eventUid"]
            userList = data["userList"]
            print(userList)
            db.markAttendanceByUserListAndEventUUID(eventUUID,userList)
            context = {
                "swal": {
                    "title": "Success",
                    "text": "Attendance marked successfully",
                    "icon": "success",
                    "butText": "Close"
                },
                "swalFlag": True,
            }
            return render(request,'webview/index.html', context=context)
        except Exception as e:
            print(e)
        print(data)


def complaint(request) :
    if request.method == "GET" :
        return render(request, "webview/complaint.html")