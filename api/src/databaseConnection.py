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