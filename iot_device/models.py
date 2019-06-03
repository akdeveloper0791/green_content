from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import time
import json
from cmsapp.models import User_unique_id
from django.db import IntegrityError
from campaign.models import Player_Campaign
from player.models import Player
from django.db import transaction

# Create your models here.

class IOT_Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    mac = models.CharField(max_length=125,blank=False,null=False,unique=True,db_index=True)
    key = models.CharField(max_length=125,blank=False,null=False,unique=True,db_index=True,default="adskite")#auto generate
    name = models.CharField(max_length=50,blank=False,null=False)
    device_type = models.CharField(max_length=50,blank=False,null=False)
    registered_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def registerPlayer(data,userId):
        try:
           data =  json.loads(data);
           uniqueKey = str(uuid.uuid4().hex[:6].upper())+str(round(time.time() * 1000))+uuid.uuid4().hex[:6];
           try:
            player = IOT_Device.objects.get(mac=data['mac'])
            
           except IOT_Device.DoesNotExist:
            player = IOT_Device(mac=data['mac'],key=uniqueKey);
                   
           player.user_id = userId;
           player.name = data["name"];
           player.device_type = data["device_type"];
           player.updated_at = timezone.now(); 
           player.save();
           return {'statusCode':0,'player':player.id,'mac':data['mac'],
           'key':player.key};
           
        except Exception as ex:
           return {'statusCode':5,'status':'unable to register - '+str(ex)};
         
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters,  - "+str(ex)}

    def getMyPlayers(userId):
      player = IOT_Device.objects.filter(user_id=userId);
      return list(player.values());

    def isMyPlayer(playerKey,userId):
      try:
        player = IOT_Device.objects.get(key=playerKey,
          user_id=userId);
        return player;
      except IOT_Device.DoesNotExist:
        return False;

class Contextual_Ads_Rule(models.Model):
    iot_device = models.ForeignKey('iot_device.IOT_Device',on_delete=models.CASCADE)
    classifier = models.CharField(max_length=125,blank=False,null=False,db_index=True)
    delay_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def createRule(iotDeviceKey,userId,players,campaigns,calssifier,delayTime,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           players =  json.loads(players);
           campaigns = json.loads(campaigns);
           #check for device
           isMyIOTDevice = IOT_Device.isMyPlayer(iotDeviceKey,userId);
           if(isMyIOTDevice==False):
            return {'statusCode':7,'status':'Invalid device'};

           #check for campaigns
           if(Player_Campaign.checkForvalidCampaigns(campaigns,userId)==False):
            return {'statusCode':7,'status':'Some of the campaigns are not found, please refresh and try again later'};
           
           #check for players
           if(Player.checkForvalidPlayers(players,userId)):
            return {'statusCode':7,'status':'Some of the players are not found, please refresh and try again later'};
           
           with transaction.atomic():
                ca_rule = Contextual_Ads_Rule();
                ca_rule.iot_device_id = isMyIOTDevice.id;
                ca_rule.classifier=calssifier;
                ca_rule.delay_time = delayTime;
                ca_rule.save();

                bulkInsertCARCampaigns = [];
                for campaignId in campaigns:
                  bulkInsertCARCampaigns.append(CAR_Campaign(car_id=ca_rule.id,campaign_id=campaignId));

                CAR_Campaign.objects.bulk_create(bulkInsertCARCampaigns);
                bulkInsertCARCampaigns.clear();

                bulkInsertCARPlayers = [];
                for playerId in players:
                  bulkInsertCARPlayers.append(CAR_Device(car_id=ca_rule.id,player_id=playerId));

                CAR_Device.objects.bulk_create(bulkInsertCARPlayers);

           return {'statusCode':0,'status':'Rule has been created'};
           
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters unable to parse,"+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Player has already some of the campaigns provided, please check and add again "+str(e)};

        except Exception as e:
            return {'statusCode':3,'status':
                "error "+str(e)};

#contextual ads rules associated campaigns
class CAR_Campaign(models.Model):
    car = models.ForeignKey('iot_device.Contextual_Ads_Rule',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)

#contextual ads rules associated DSP(signages)
class CAR_Device(models.Model):
    car = models.ForeignKey('iot_device.Contextual_Ads_Rule',on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
