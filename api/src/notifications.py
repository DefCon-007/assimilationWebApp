# Send to single device.
from pyfcm import FCMNotification
from django.conf import settings
push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
from api.src import utils
from api.src import databaseConnection as db
# OR initialize with proxies

proxy_dict = {
          "http"  : "http://127.0.0.1",
          "https" : "http://127.0.0.1",
        }
push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

# registration_id = "<device registration_id>"
# message_title = "Uber update"
# message_body = "Hi john, your customized news for today is ready"
# result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
def sendNotification(grp,msg,title) :
# Send to multiple devices by passing a list of ids.
    registration_ids = db.getlistOfPushNotificationIdsFromAudienceGroup(grp)
    valid_registration_ids = push_service.clean_registration_ids(registration_ids)
    # print(f"RegIds {registration_ids}, validIds {valid_registration_ids}")
    # message_title = "New Event"
    # message_body =
    if valid_registration_ids :
        result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=title, message_body=msg)
        print (result)
    # print (result)