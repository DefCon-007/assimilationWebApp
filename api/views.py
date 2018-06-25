from django.http import HttpResponse, JsonResponse
from api.src import utils
# Create your views here.
from rest_framework.decorators import api_view


@api_view(['POST'])
def login(request) :
    data = request.data
    try :
        username = data["username"]
        password = data["password"]
    except KeyError :
        return HttpResponse("Bad Request",status=400)
    user = utils.authenticateCredentials(username,password)
    if user is not None :
        groupList = list()
        for grp in user.groups.all() :
            grpName = grp.name
            if "dep" in grpName or "hall" in grpName :
                groupList.append(grpName)
        return JsonResponse({"name": user.get_short_name(), "groups" : ",".join(groupList)},status=200)
    else :
        return HttpResponse("Invalid credentials",status=401)