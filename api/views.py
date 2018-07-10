from django.http import HttpResponse, JsonResponse
from api.src import utils
from api.src import databaseConnection as db
# Create your views here.
from rest_framework.decorators import api_view
from assimilation import settings
import json
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
        validHelpersList = db.getHelpersFromGroupName(grpNameList, request.user.username)
        helperListForView = utils.getHelperFormattedListFromQuerySet(validHelpersList)
        return JsonResponse({"name": user.get_short_name(), "audience" : json.dumps({"key" :grpNameMappedList[1], "value":grpNameMappedList[0] }), "token" : token, "helpers" : json.dumps(helperListForView)},status=200)
    else :
        return HttpResponse("Invalid credentials. Please try again!",status=401)

@api_view(["POST"])
def createEvent(request) :
    data = request.data
    print(request.data)
    print(type(request.POST.getlist('helpers')))
    print(request.POST.getlist('helpers'))
    dictToReturn = {
        "status" : "st",
        "statusDescription" : "desc",
        "fillFormFlag": True,
        "title": "1",
        "description": "2",
        "venue": "3",
        "date": "4",
        "time": "5",
    }
    return  JsonResponse(dictToReturn,status=200)