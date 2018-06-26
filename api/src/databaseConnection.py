from django.contrib.auth.models import User, Group

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

# def addNewEvent(title,description,venue,date,time,audience,helpers) :
