from django.db import models
from datetime import datetime as dt
import json
import datetime

# Create your models here.
class License_Device(models.Model):
    mac = models.CharField(max_length=50,primary_key=True)
    status = models.SmallIntegerField(default=1)#1->active,0->expired
    expiry_date= models.DateTimeField()
    mobile_number = models.CharField(max_length=10,null=True)
    org_email = models.CharField(max_length=50,null=True)
    registered_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    def registerPlayer(data):
        try:
           data =  json.loads(data);
           try:
            player = License_Device.objects.get(mac=data['mac'])
            canUpdate = False;
            if("mobile_number" in data and 
                data["mobile_number"] != player.mobile_number):
              player.mobile_number = data["mobile_number"];
              canUpdate = True;
            if("org_email" in data and 
              data["org_email"] != player.org_email):
              player.org_email = data["org_email"];
            if(canUpdate):
              player.save();
           except License_Device.DoesNotExist:
            player = License_Device(mac=data['mac']);
            currentDate = dt.now();
            player.expiry_date = currentDate+datetime.timedelta(days=15);
            player.registered_date = currentDate;
            player.updated_date = currentDate;
            player.status = 1;
            if("mobile_number" in data["mobile_number"]):
              player.mobile_number = data["mobile_number"];
            if("org_email" in data["org_email"]):
              player.org_email = data["org_email"];
            player.save();
           

           return {'statusCode':0,'status':player.status,'mac':data['mac'],
           'expiry_date':player.expiry_date};
        except Exception as ex:
           return {'statusCode':5,'status':'unable to register - '+str(ex)};
         
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters,  - "+str(ex)}