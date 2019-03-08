from django.db import models
from django.conf import settings
import datetime
from datetime import datetime as dt
import json


# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    mac = models.CharField(max_length=20,blank=False,null=False)
    name = models.CharField(max_length=25,blank=False,null=False)
    status = models.SmallIntegerField(default=0)#0->in trail, 1->activated, -1->expired
    fcm_id = models.CharField(max_length=125)
    expiry_date = models.DateTimeField()
    registered_at = models.DateTimeField(default=datetime.datetime.now())
    activated_by = models.CharField(max_length=25,default=0)#0 is self

    class Meta(object):
        unique_together=[
        ['user','mac']
        ]

    def __str__(self):
        return self.mac

    def registerPlayer(data,userId):
        try:
           data =  json.loads(data);
           try:
            player = Player.objects.get(user_id=userId,mac=data['mac'])
            
           except Player.DoesNotExist:
            player = Player(user_id=userId,mac=data['mac']);
            player.expiry_date = dt.now() + datetime.timedelta(days=15);
           player.name = data["name"];
           player.fcm_id = data['fcm_id'];
           player.save();
           return {'statusCode':0,'status':player.status,'player':player.id};
        except Exception as ex:
           return {'statusCode':5,'status':'unable to register - '+str(ex)};


           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};