from django.contrib.auth.models import User, Group
from api.models import event

def getListofAllDepAndHallGroups() :
    allGroups = Group.objects.all()
    depGroupList = list()
    hallGroupList = list()

    for data in allGroups :
        try :
             grpNameList = data.name.split("_")
             if grpNameList[0] == "dep" :
                 depGroupList.append(data.name)
             elif grpNameList[0] == "hall" :
                 hallGroupList.append(data.name)
        except IndexError :
            pass
    return depGroupList,hallGroupList

def getHelpersFromGroupName(grpNameList):
    """
    Returns a list of User objects from the groups supplied and admin group
    :param grpNameList: A list of group names
    :return:
    """
    userList = list()
    allAdmins = User.objects.filter(groups__name="admin")
    for grpName in grpNameList :
        if grpName == "admin" :
            pass
        try :
            userList.extend(allAdmins.filter(groups__name=grpName))
        except ValueError :
            print("Unknown grp found")
    return userList

def addNewEvent(title,description,venue,datetimeobj,audience,helpers,createdBy) :
    data = event()
    data.title = title
    data.description = description
    data.venue = venue
    data.datetime = datetimeobj
    data.audience = audience
    data.createdBy = createdBy
    for helper in helpers :
        user = getUserFromUsername(helper)
        if user :
            data.helpers.add(user)
    data.save()



def getUserFromUsername(username) :
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as e:
        return None
