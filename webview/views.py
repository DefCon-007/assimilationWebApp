import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.src import utils
from django.http import JsonResponse
import traceback
from api.src import databaseConnection as db
# Create your views here.
from rest_framework.decorators import api_view
from assimilation import settings
from assimilation.settings import  LOGGER
@login_required()
def index(request) :
    LOGGER.info("Test log in index")
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
                try :
                    helpers = request.POST.getlist('helpers')
                except KeyError :
                    helpers = None
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
    if request.user.has_perm('api.add_event') :
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
    else :
        return render(request, "webview/errorPage.html", {
            "d1": 4, "d2": 0, "d3": 1, "msg": "Sorry! You are not authorized for this."
        })
@login_required()
@api_view(["GET","POST"])
def complaint(request) :
    if request.user.has_perm('api.add_complaint') :
        if request.method == "GET" :
            data = request.query_params
            try :
                eventUUID = data["eventId"]
                event = db.getEventByUUID(eventUUID)
                return render(request,"webview/complaint.html", {"eventUID" : eventUUID, "eventTitle" : event.title, "eventDate" : event.datetime.strftime("%d/%m/%Y")})

            except KeyError as e:
                return render(request, "webview/errorPage.html", {
                "d1" : 4, "d2" : 0 , "d3" : 0, "msg" : "Bad request! Try creating complaint from Upcoming Events page."
            })
        else :
            #A complaint was submitted and now it will saved to database
            data = request.data
            print(data)
            try :
                eventUUID = data["eventUUID"]
                message= data["message"]
                event = db.getEventByUUID(eventUUID)
                user = request.user
                status = db.addNewComplaintByEventAndUser(message,event,user)
                if status :
                    context = {
                        "swal": {
                            "title": "Success",
                            "text": "Complaint submitted successfully",
                            "icon": "success",
                            "butText": "Close"
                        },
                        "swalFlag": True,

                    }
                else :
                    context = {
                        "swal": {
                            "title": "Error",
                            "text": "Unable to submit complaint. Please try again.",
                            "icon": "error",
                            "butText": "Close"
                        },
                        "swalFlag": True,

                    }
            except KeyError :
                context = {
                    "swal": {
                        "title": "Error",
                        "text": "Unable to submit complaint. Please try again.",
                        "icon": "error",
                        "butText": "Close"
                    },
                    "swalFlag": True,

                }
            return render(request, "webview/index.html", context=context)
            # try :
            #     eventUUID = data["eventUUID"]

    else :
        return render(request, "webview/errorPage.html", {
            "d1": 4, "d2": 0, "d3": 1, "msg": "Sorry! You are not authorized for this."
        })

@api_view(["GET"])
def allComplaints(request):
    allComplaints = db.getAllFormatedComplaintsDict()
    return  render(request,"webview/allcomplaints.html", {
        "allComplaints" : allComplaints
    })
    pass

@api_view(["GET"])
def changeComplaintStatus(request) :
    try :
        data = request.query_params
        status = db.changeComplaintStatusByComplaintId(data['complaintId'])
        if status :
            return JsonResponse({"status": True}, status=200)
        else :
            return JsonResponse({"status": False}, status=200)
    except Exception as e :
        print(e)
        return JsonResponse({"status": False}, status=200)


def custom404ErrorPage(request,exception) :
    return render(request, "webview/errorPage.html", {
        "d1": 4, "d2": 0, "d3": 4, "msg": "Sorry! Page not found."
    }, status=404)

def custom500ErrorPage(request,exception) :
    return render(request, "webview/errorPage.html", {
        "d1": 5, "d2": 0, "d3": 0, "msg": "Sorry! Server error. Please try again"
    }, status=500)

def custom403ErrorPage(request,exception) :
    return render(request, "webview/errorPage.html", {
        "d1": 4, "d2": 0, "d3": 3, "msg": "Sorry! You are not authorized for this"
    }, status=403)

def custom400ErrorPage(request,exception) :
    return render(request, "webview/errorPage.html", {
        "d1": 4, "d2": 0, "d3": 0, "msg": "Sorry! Bad request"
    }, status=400)
