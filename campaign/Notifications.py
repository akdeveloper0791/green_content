from django.core.mail import send_mail
import threading
from django.core import mail
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

class SendCampDeleteNotification(threading.Thread):
    def __init__(self, userId,message):
        self.userId = userId
        self.message = message
        threading.Thread.__init__(self)

    def run (self):
        #get user email and send email 
         user = User.objects.get(id=self.userId);
         with mail.get_connection() as connection:
            mail.EmailMessage(
            "Campaign delete notification", self.message, "contact@adskite.com", [user.email],
            connection=connection,
            ).send()
         #send_mail("Campaign delete notification", self.message, "contact@adskite.com", [user.email])
        
class SendEmail:
    def sendEmail(userId,message):
        try:
         user = User.objects.get(id=userId);
         return send_mail("Campaign delete notification", message, "adskitedeveloper@gmail.com", [user.email],
          )
         ''''''
            
        except User.DoesNotExist as e:
           return ''' user not found ''';
