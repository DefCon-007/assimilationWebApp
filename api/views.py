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
        username = data["username"]
        password = data["password"]
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
        return JsonResponse({"name": user.get_short_name(), "audience" : json.dumps({"key" :grpNameMappedList[1], "value":grpNameMappedList[0] }), "token" : token, "helpers" : json.dumps(helperListForView)},status=200)
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
            status = False
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