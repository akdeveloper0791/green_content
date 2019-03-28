from django.db import models
from datetime import datetime as dt
import json
import datetime

# Create your models here.
class License_Device(models.Model):
    mac = models.CharField(max_length=50,primary_key=True)
    status = models.SmallIntegerField(default=1)#1->active,0->expired
    expiry_date= models.DateTimeField()
    registered_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    def registerPlayer(data):
        try:
           data =  json.loads(data);
           try:
            player = License_Device.objects.get(mac=data['mac'])
            
           except License_Device.DoesNotExist:
            player = License_Device(mac=data['mac']);
            currentDate = dt.now();
            player.expiry_date = currentDate + datetime.timedelta(days=15);
            player.registered_date = currentDate;
            player.updated_date = currentDate;
           
            player.save();
           return {'statusCode':0,'status':player.status,'mac':data['mac']};
        except Exception as ex:
           return {'statusCode':5,'status':'unable to register - '+str(ex)};
         
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters,  - "+str(ex)}