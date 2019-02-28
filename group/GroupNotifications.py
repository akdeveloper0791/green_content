import threading
from django.core import mail
from django.contrib.auth.models import User
from django.template.loader import  get_template
from django.core.mail import EmailMessage

class SendGroupAssignNotifications(threading.Thread):
    def __init__(self, members,gId,gName,userId):
        self.members = members
        self.gId = gId
        self.gName = gName
        self.userId = userId
        threading.Thread.__init__(self)

    def run (self):
        try:
            user = User.objects.get(id=self.userId);
            ctx = {
            'creator_name': user.username,
            'group_name': self.gName,
            'url':'http://127.0.0.1:8000/groups/approve/{}'.format(self.gId)
            } 
            message = get_template('groups/assign_new_member_email_notification.html').render({'info':ctx})
            to = self.members;
            from_email = "contact@adskite.com"
            with mail.get_connection() as connection:
                msg = EmailMessage("Green Content Group Assign Notification", message, to=to, from_email=from_email,
                    connection=connection)
                msg.content_subtype = 'html'
                response = msg.send();
                print(response);
        except User.DoesNotExist:
            print("Creator info not found");