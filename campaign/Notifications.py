from django.core.mail import send_mail
import threading
from django.contrib.auth.models import User

class SendCampDeleteNotification(threading.Thread):
    def __init__(self, userId,message):
        self.userId = userId
        self.message = message
        threading.Thread.__init__(self)

    def run (self):
        #get user email and send email 
        try:
         user = User.objects.get(id=self.userId);
         send_mail("Campaign delete notification", self.message, "contact@adskite.com", [user.email],
            fail_silently=True)
        except User.DoesNotExist as e:
            ''' user not found ''';