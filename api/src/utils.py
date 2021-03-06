from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from api.models import  event

class eventForm(ModelForm) :
    class Meta :
        model = event
        fields = ['title','description','venue','datetime']

def authenticateCredentials(username,password) :
    """
    Authenticates set of credentials on a user model
    :param username:
    :param password:
    :return: User object if authentication successful else None
    """
    user = authenticate(username=username, password=password)
    return user

def isMember(user, groupName) :
    return user.groups.filter(name=groupName).exists()


def getHelperFormattedListFromQuerySet(helperList) :
    formattedHelperList = list()
    for helper in helperList:
        formattedHelperList.append({
            "username": helper.username,
            "fullname": helper.get_full_name()
        })
    return formattedHelperList

def convertAttendanceObjectListToListOfDict(attendanceObjList) :
    listToReturn = list()
    for data in attendanceObjList :
        listToReturn.append({
            "roll" : data.user.username,
            "name" : data.user.get_full_name(),
            "attendanceStatus" : True if data.attendanceStatus else False
        })
    newlist = sorted(listToReturn, key=lambda k: k['roll'])
    return newlist
# def addNewEvent() :
#