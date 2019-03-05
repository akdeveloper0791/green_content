from django.core.management.base import BaseCommand
import threading
from group.models import GroupMemberAssignNotification, GroupCampaignAssignNotification
from django.core import mail
from django.core.mail import EmailMessage
import json
import time

class Command(BaseCommand):
    help = 'Sends Group assign notifications'

    def handle(self, *args, **kwargs):
        thread1 = GroupMemberAssignNotifications();
        thread1.start();
        

        thread2 = GroupCampaignAssignNotifications();
        thread2.start();
        
        #thread1.join();
        #thread2.join();



class GroupMemberAssignNotifications(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #get notifications 
        notifications = GroupMemberAssignNotification.objects.all().order_by('id')[:100];
        if notifications.exists():
            print("total notifications\{} ".format(notifications.count()),flush=True)
            
            from_email = "contact@adskite.com" 
            try:
                with mail.get_connection() as connection:
                    for notification in notifications.iterator():
                        msg = EmailMessage("Green Content Group Assign Notification", notification.message, to=json.loads(notification.member), from_email=from_email,
                        connection=connection)
                        msg.content_subtype = 'html'
                        response = msg.send();
                        print(notification.member,flush=True);
                        print(response,flush=True);
                        if(response==1):
                            notification.delete();
            except Exception as e:
                print("Error in sending notifications to assigned"+str(e),flush=True);
            
        else:
            print("No notifications found",flush=True);

        #sleep 
        time.sleep(60)


class GroupCampaignAssignNotifications(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #get notifications 
        notifications = GroupCampaignAssignNotification.objects.all().order_by('id')[:100];
        if notifications.exists():
            print("total campaign notifications\{} ".format(notifications.count()),flush=True)
            
            from_email = "contact@adskite.com" 
            try:
                with mail.get_connection() as connection:
                    for notification in notifications.iterator():
                        
                        members = json.loads(notification.member);
                        to = [];
                        for member in members:
                            to.append(member['email']);
                        msg = EmailMessage("GreenContent New Campaign Notification", notification.message, to=to, from_email=from_email,
                        connection=connection)
                        msg.content_subtype = 'html'
                        response = msg.send();
                        print(notification.member,flush=True);
                        print(response,flush=True);
                        if(response==1):
                            notification.delete();
            except Exception as e:
                print("Error in sending campaign notifications to assigned"+str(e),flush=True);
            
        else:
            print("No campaign notifications found",flush=True);

        #sleep 
        time.sleep(60)