from django.core.management.base import BaseCommand
from django.utils import timezone
from group.models import GroupMemberAssignNotification
from django.core import mail
from django.core.mail import EmailMessage
import json

class Command(BaseCommand):
    help = 'Sends Group assign notifications'

    def handle(self, *args, **kwargs):
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