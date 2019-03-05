from django.core.management.base import BaseCommand
import threading
from group.models import GroupMemberAssignNotification
from django.core import mail
from django.core.mail import EmailMessage
import json
import time

class Command(BaseCommand):
    help = 'Sends Group assign notifications'

    def handle(self, *args, **kwargs):
        thread1 = Thread1();
        thread1.start();
        

        thread2 = Thread2();
        thread2.start();
        
        #thread1.join();
        #thread2.join();



class Thread1(threading.Thread):
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
                        notification.delete();
            except Exception as e:
                print("Error in sending notifications to assigned"+str(e),flush=True);
            
        else:
            print("No notifications found",flush=True);


class Thread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for i in range(1000):
            print("Thread - "+str(2));
            ++i;