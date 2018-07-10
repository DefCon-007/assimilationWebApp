from django.contrib.auth.models import User, Group
from api.models import event, attendance, complaint,UserDeviceIdAndAuthToken
from assimilation import settings
from api.src import utils
import datetime
from raven.contrib.django.raven_compat.models import client
import uuid
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

def getHelpersFromGroupName(grpNameList,requestUserName):
    """
    Returns a list of User objects from the groups supplied and admin group
    :param grpNameList: A list of group names
    :return:
    """
    userList = list()
    allAdmins = User.objects.filter(groups__name=settings.ATTENDANCE_TAKER_GROUP_NAME).exclude(username=requestUserName)
    for grpName in grpNameList :
        if grpName == settings.ATTENDANCE_TAKER_GROUP_NAME :
            continue
        elif grpName == settings.SUPER_ADMINS_GROUP_NAME :
            userList.extend(allAdmins.filter(groups__name=settings.GYMKHANA_GSEC_GROUP_NAME))
        else :
            try :
                userList.extend(allAdmins.filter(groups__name=grpName))
            except ValueError as e:
                settings.LOGGER.exception(f"Following exception occured while getting helper from group name{grpName}\n{e}")
                print("Unknown grp found")
    return userList

#Attendance
def addStudentsInAttendanceTable(audience,event) :
    # userList = list()
    if audience == settings.SUPER_ADMINS_GROUP_NAME or audience == settings.GYMKHANA_GSEC_GROUP_NAME :
        userList = User.objects.filter(groups__name='student')
    else :
        userList = User.objects.filter(groups__name='student').filter(groups__name=audience)
    # for audience in audienceList :
    #     userList.extend(User.objects.filter(groups__name='student').filter(groups__name=audience))
    for user in userList :
        attendanceObject = attendance()
        attendanceObject.event = event
        attendanceObject.user = user
        attendanceObject.save()
def getAttendanceObjectListFromEvent(event):
    return event.eventName.get_queryset()
def markAttendanceByUserListAndEventUUID(uid,userList):
    particularEvent = getEventByUUID(uid)
    if particularEvent :
        for user,status in userList.items() :
            userObj = getUserFromUsername(user)
            if userObj :
                attendanceObj = attendance.objects.get(event=particularEvent, user=userObj)
                if attendanceObj :
                    attendanceObj.attendanceStatus = status
                    attendanceObj.save()



#EVENT
def addNewEvent(title,description,venue,datetimeobj,audience,helpers,createdBy) :
    data = event()
    data.title = title
    data.description = description
    data.venue = venue
    data.datetime = datetimeobj
    data.createdBy = createdBy
    try :
        grp = Group.objects.get(name=audience)
        data.save()
        data.audience.add(grp)
    except Exception as e:
        settings.LOGGER.exception(f"While getting group for {audience} following exception occurred \n{e}")
        return False
    if helpers :
        for helper in helpers :
            user = getUserFromUsername(helper)
            if user :
                data.helpers.add(user)
    data.save()
    addStudentsInAttendanceTable(audience,data)
    return True

def editEvent(eventId,title,description,venue,datetimeobj,helpersList) :
    try :
        data = event.objects.get(id=eventId)
        data.title = title
        data.description = description
        data.venue = venue
        data.datetime = datetimeobj
        data.helpers.clear()
        data.save()
        if helpersList :
            for helper in helpersList :
                user = getUserFromUsername(helper)
                if user :
                    data.helpers.add(user)
        data.save()
        return True
    except Exception as e :
        settings.LOGGER.exception(f"While editing event({eventId}) following exception occured\n{e}")
        return False
def getEventFromUsername(username) :
    user = getUserFromUsername(username)
    formattedEventList = list()
    if user :
        if utils.isMember(user,settings.SUPER_ADMINS_GROUP_NAME) :
            eventListOwner = user.owned_events.get_queryset()
            formattedEventList.extend(getEventDictListFromEventList(eventListOwner, "Owner"))
            eventList = event.objects.filter().exclude(createdBy=user)
            formattedEventList .extend(getEventDictListFromEventList(eventList, ""))
            return formattedEventList
        if user.has_perm('api.add_event') :
            #this implies user is a attendance taker
            eventList = user.owned_events.get_queryset()
            formattedEventList.extend(getEventDictListFromEventList(eventList, "Owner"))
            eventList = user.manytomanyevents.get_queryset()
            formattedEventList.extend(getEventDictListFromEventList(eventList, "Helper"))
            return formattedEventList
        else :
            #this means user is a student
            for grp in user.groups.all() :
                formattedEventList.extend(getEventDictListFromEventList(grp.group_events.get_queryset(),"student" ))
            return formattedEventList
    else :
        return []
def getEventDictListFromEventList(eventList,role) :
    listToReturn = list()
    for event in eventList:
        Eventdatetime = event.datetime
        helperList = list()
        for helper in event.helpers.all():
            helperList.append(f"{helper.get_full_name()} ({helper.username})")
        audienceList=list()
        for audience in event.audience.all() :
            try :
                audienceList.append(settings.GROUPS_MAP[audience.name])
            except Exception as e:
                settings.LOGGER.exception(f"Following exception occured while getting mapped audience name for upcoming event\n{e}")
        if Eventdatetime > datetime.datetime.now() :
            deleteFlag = True
        else :
            deleteFlag = False
        listToReturn.append({
        "title": event.title,
        "description": event.description,
        "venue": event.venue,
        "audience": ",".join(audienceList),
        "date": Eventdatetime.strftime('%d/%m/%Y'),
        "time": Eventdatetime.strftime('%H:%M'),
        "createdBy": f"{event.createdBy.get_full_name()} ({event.createdBy.username})",
        "helpers": helperList,
        "role": role,
        "uid" : str(event.id),
        "deleteFlag" : deleteFlag
        })
    return listToReturn

def getEventByUUID(uid) :
    try :
        events = event.objects.get(id=uid)
        return events
    except Exception as e :
        print(e)
        return None

def deleteEventByUid(uid) :
    try :
        eventFromUid = event.objects.get(id=uid)
        eventFromUid.delete()
        return True
    except Exception as e:
        settings.LOGGER.exception(f"Following exception occured while deleting event {uid} \n{e}")
        return False

#Complaints
def addNewComplaintByEventAndUser(message,event,user) :
    if event and user :
        data = complaint()
        data.message = message
        data.event = event
        data.user = user
        data.createdDateTime = datetime.datetime.now()
        data.save()
        return True
    else :
        return False
def getAllFormatedComplaintsDict() :
    allComplaintsList = complaint.objects.filter()
    allComplaintFormattedDictList = list()
    for c in allComplaintsList :
        event = c.event
        user = c.user
        helperList = list()
        for helper in event.helpers.all():
            helperList.append(f"{helper.get_full_name()} ({helper.username})")
        allComplaintFormattedDictList.append({
            "eventCreatedBy" : f"{event.createdBy.get_full_name()} ({event.createdBy.username})",
            "eventDate" : event.datetime.strftime("%d/%m%Y"),
            "eventHelpers" : helperList,
            "eventVenue" : event.venue,
            "eventTitle" : event.title,
            "complaintBy" : f"{user.get_full_name()} ({user.username})",
            "complaintDateTime" : c.createdDateTime.strftime("%Y-%m-%d at %H : %M"),
            "complaintMessage" : c.message,
            "complaintResolutionStatus" : c.resolutionStatus,
            "complaintId" : c.id
        })
    return allComplaintFormattedDictList
def changeComplaintStatusByComplaintId(complaintId) :
    specificComplaint = complaint.objects.get(id=complaintId)
    if specificComplaint :
        specificComplaint.resolutionStatus = True
        specificComplaint.save()
        return True
    else :
        return False

#UserDeviceIdAndAuthToken
def getUserDeviceIdAndAuthTokenObjectByUser(user,deviceId)  :
    data = user.authTable.get_queryset()
    token = uuid.uuid4()
    if data :
        authObj = data[0]
        print(f"existing user {authObj.token}")
        authObj.token =token
        authObj.deviceId = deviceId
        try :
            authObj.save()
            status = True
        except Exception as e :
            settings.LOGGER.exception(f"Following exception occured in saving new auth object for {user.username}, deviceId {deviceId}\n{e}")
            status = False
        return token, status
    else :
        print("new user")
        authObj = UserDeviceIdAndAuthToken()
        authObj.token = token
        authObj.user = user
        authObj.deviceId = deviceId
        try :
            authObj.save()
            status = True
        except Exception as e :
            settings.LOGGER.exception(f"Following exception occured in saving new auth object for {user.username}, deviceId {deviceId}\n{e}")
            status = False
        return token, status

def getUserFromToken(token) :
    try :
        user = UserDeviceIdAndAuthToken.objects.get(token=token).user
        return user
    except Exception as e :
        settings.LOGGER.exception(f"Following exception occurred while getting user from token {token}\n{e}")
        client.captureException()
        return None
#EXTRAS
def getUserFromUsername(username) :
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as e:
        return None
