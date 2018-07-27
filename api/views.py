from django.http import HttpResponse, JsonResponse
from api.src import utils
from api.src import databaseConnection as db
# Create your views here.
from rest_framework.decorators import api_view
from assimilation import settings
import datetime
import json
from raven.contrib.django.raven_compat.models import client
@api_view(['POST'])
def login(request) :
    data = request.data
    try :
        username = data["username"].strip()
        password = data["password"].strip()
        deviceId = data["deviceId"]
    except KeyError :
        return HttpResponse("Bad Request. Contact administrator",status=400)
    user = utils.authenticateCredentials(username,password)
    if user is not None :
        token, status = db.getUserDeviceIdAndAuthTokenObjectByUser(user, deviceId)
        if not status :
            #Unable to save error response
            return HttpResponse("Invalid credentials. Please try again!", status=401)
        grpNameList = list()
        grpNameMappedList = list()
        for g in user.groups.all():
            grpNameList.append(g.name)
            try:
                mapName = settings.GROUPS_MAP[g.name]
                grpNameMappedList.extend([mapName, g.name])
            except Exception as e:
                pass
        validHelpersList = db.getHelpersFromGroupName(grpNameList, user.username)
        helperListForView = utils.getHelperFormattedListFromQuerySet(validHelpersList)
        return JsonResponse({"name": user.get_short_name(),
                             "audience" : json.dumps({"key" :grpNameMappedList[1],
                                                      "value":grpNameMappedList[0] }),
                                                        "token" : token,
                                                        "helpers" : json.dumps(helperListForView),
                                                        "isAttendanceTaker" : utils.isMember(user, settings.ATTENDANCE_TAKER_GROUP_NAME),
                                                        "isSuperAdmin" : utils.isMember(user,settings.SUPER_ADMINS_GROUP_NAME),
                                                        "isStudent" : utils.isMember(user,settings.STUDENT_GROUP_NAME),
                                                        "isGymakhanaGsec": utils.isMember(user,settings.GYMKHANA_GSEC_GROUP_NAME) },status=200)
    else :
        return HttpResponse("Invalid credentials. Please try again!",status=401)

@api_view(["POST"])
def createEvent(request) :
    try:
        data = request.data
        title = data["title"]
        description = data["description"]
        venue = data["venue"]
        date = data["date"]
        time = data["time"]
        token = data["token"]
        datetimestring = date + "|" + time
        datetimeobject = datetime.datetime.strptime(datetimestring, "%d-%m-%Y|%H : %M")
        audience = data["audience"]
        user = db.getUserFromToken(token)
        if user :
            try:
                helpers = request.POST.getlist('helpers')
            except KeyError:
                # No need to log this as it shows no helpers were needed
                helpers = None
            status = db.addNewEvent(title=title, description=description, venue=venue, datetimeobj=datetimeobject,
                                    audience=audience, helpers=helpers, createdBy=user)
            if status :
                return JsonResponse({"success":True, "message" :"Event created successfully" }, status=200)
            else :
                return JsonResponse({"success" : False ,"message" : "Some error occurred. Please try again later!"}, status=200)
        else :
            pass
    except Exception as e:
        settings.LOGGER.exception(f"Following exception occured in createEvnt api POST {e}")
        client.captureException()
        return  JsonResponse({"status" : "Sorry! Server error. Please try again"},status=500)

@api_view(["POST"])
def upcomingevent(request) :
    try :
        data = request.data
        token = data["token"]
        user = db.getUserFromToken(token)
        if user :
            eventsList = db.getEventFromUsername(user.username)
            print(eventsList)
            return JsonResponse({"eventData" : eventsList}, status=200)
        else :
            pass
    except Exception as e :
        client.captureException(e)
        settings.LOGGER(f"Following exception occured in upcoming event {e}")
    pass

@api_view(["POST"])
def markSingleUserAttendance(request) :
    try :
        data = request.data
        eventUid = data["eventUid"]
        username = data["username"].strip()
        attendancestatus = data["status"].strip().lower()
        if attendancestatus == "true" :
            attendancestatus = True
        else :
            attendancestatus = False
        status =  db.markAttendanceByUserAndEventUUID(eventUid,username, attendancestatus)
        if status :
            return JsonResponse({"attendanceStatus" : True, "message":"Attendance marked successfully"},status=200)
        else :
            return JsonResponse({"attendanceStatus": False, "message": "Unable to mark attendance"}, status=200)
    except Exception as e :
        settings.LOGGER.exception(f"Following exception occured while marking attendance for single user\n{e}")
        return JsonResponse({"attendanceStatus": False, "message": "Unable to mark attendance"}, status=200)

@api_view(["POST"])
def getStudentAttendanceList(request) :
    try :
        data = request.data
        eventUid = data["eventUid"]
        event = db.getEventByUUID(eventUid)
        attendanceList = utils.convertAttendanceObjectListToListOfDict(db.getAttendanceObjectListFromEvent(event))
        return JsonResponse({"attendanceList" : attendanceList}, status=200)
    except Exception as e :
        pass

@api_view(["POST"])
def changePassword(request) :
    try :
        data = request.data
        newPassword = data["password"]
        token = data["token"]
        pwdChangeStatus = db.changePasswordByToken(token,newPassword)
        if pwdChangeStatus :
            return JsonResponse({"passwordChangeStatus": True}, status=200)
        else :
            return JsonResponse({"passwordChangeStatus": False}, status=200)
    except Exception as e :
        settings.LOGGER.exception(f"Following exception occurred while changing user password in api\n{e}")
        return  JsonResponse({"passwordChangeStatus" : False}, status=200)


@api_view(["POST"])
def deleteEvent(request) :
    try :
        data = request.data
        eventUID = data["eventUid"]
        token = data["token"]
        user = db.getUserFromToken(token)
        event = db.getEventByUUID(eventUID)
        if not user or not event:
            return JsonResponse({"deleteStatus" : False},status=200)
        else :
            creator = event.createdBy
            if user != creator :
                return JsonResponse({"deleteStatus": False}, status=200)
        status = db.deleteEventByUid(eventUID)
        if status :
            return JsonResponse({"deleteStatus": True}, status=200)
        else :
            return JsonResponse({"deleteStatus": False}, status=200)
    except Exception as e:
        settings.LOGGER.exception(f"Following exception occured in delete event view\n {e}")
        return JsonResponse({"deleteStatus": False}, status=200)

@api_view(["POST"])
def createComplaint(request):
    try :
        data = request.data
        eventUid = data["eventUID"]
        token = data["token"]
        complaint = data["complaint"]
        user = db.getUserFromToken(token)
        event = db.getEventByUUID(eventUid)

        if not user or not event:
            return JsonResponse({"complaintStatus": False}, status=200)
        if not user.has_perm('api.add_complaint') :
            return JsonResponse({"complaintStatus": False}, status=200)

        status = db.addNewComplaintByEventAndUser(complaint, event, user)
        if status :
            return JsonResponse({"complaintStatus": True}, status=200)
        else :
            return JsonResponse({"complaintStatus": False}, status=200)

    except Exception as e :
        settings.LOGGER.exception(f"Following error occured in raising complaint\n{e}")
        return JsonResponse({"complaintStatus": False},status=200)