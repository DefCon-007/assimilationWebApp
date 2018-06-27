from django.contrib.auth.models import User, Group
from api.models import event, attendance
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


#EVENT
def addNewEvent(title,description,venue,datetimeobj,audiences,helpers,createdBy) :
    data = event()
    data.title = title
    data.description = description
    data.venue = venue
    data.datetime = datetimeobj
    data.createdBy = createdBy
    data.save()
    for audience in audiences :
        grp = Group.objects.get(name=audience)
        print(grp)
        data.audience.add(grp)
    for helper in helpers :
        user = getUserFromUsername(helper)
        if user :
            data.helpers.add(user)
    data.save()
    addStudentsInAttendanceTable(audiences,data)

def addStudentsInAttendanceTable(audienceList,event) :
    userList = list()
    for audience in audienceList :
        userList.extend(User.objects.filter(groups__name='student').filter(groups__name=audience))
    for user in userList :
        attendanceObject = attendance()
        attendanceObject.event = event
        attendanceObject.user = user
        attendanceObject.save()

def getEventFromUsername(username) :
    user = getUserFromUsername(username)
    formattedEventList = list()
    if user :
        eventList = user.owned_events.get_queryset()
        formattedEventList.extend(getEventDictListFromEventList(eventList, "Owner"))
        eventList = user.manytomanyevents.get_queryset()
        formattedEventList.extend(getEventDictListFromEventList(eventList, "Helper"))
        return formattedEventList
    else :
        return []
def getEventDictListFromEventList(eventList,role) :
    listToReturn = list()
    for event in eventList:
        datetime = event.datetime
        helperList = list()
        for helper in event.helpers.all():
            helperList.append(f"{helper.get_full_name()} ({helper.username})")
        audienceList=list()
        for audience in event.audience.all() :
            audienceList.append(audience.name)
        listToReturn.append({
        "title": event.title,
        "description": event.description,
        "venue": event.venue,
        "audience": ",".join(audienceList),
        "date": datetime.strftime('%d/%m/%Y'),
        "time": datetime.strftime('%H:%M'),
        "createdBy": f"{event.createdBy.get_full_name()} ({event.createdBy.username})",
        "helpers": helperList,
        "role": role
        })
    return listToReturn

def getUserFromUsername(username) :
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as e:
        return None
