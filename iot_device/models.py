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
from django.db import transaction, connection

# Create your models here.
def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

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

    def deleteRule(ruleId,userId,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           #check for device
           ruleInfo = Contextual_Ads_Rule.objects.get(id=ruleId,iot_device__user_id=userId);
           ruleInfo.delete();
           return {'statusCode':0,'status':'Rule has been deleted'};

        except Contextual_Ads_Rule.DoesNotExist as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters rule not found,"+str(ex)};
        
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters unable to parse,"+str(ex)};

        except Exception as e:
            return {'statusCode':3,'status':
                "error "+str(e)};

#contextual ads rules associated campaigns
class CAR_Campaign(models.Model):
    car = models.ForeignKey('iot_device.Contextual_Ads_Rule',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)
    
    class Meta(object):
        unique_together = [
        ['car','campaign']
        ]

    def assignNew(ruleId,userId,campaigns,isWeb):
          if(isWeb == False):
              userId = User_unique_id.getUserId(userId);
              if(userId == False):
                  return {'statusCode':1,'status':
                  "Invalid session, please login"};
          
          try:
             #check for device
             ruleInfo = Contextual_Ads_Rule.objects.get(id=ruleId,iot_device__user_id=userId);
             campaigns = json.loads(campaigns);
             #check for campaigns
             if(Player_Campaign.checkForvalidCampaigns(campaigns,userId)==False):
              return {'statusCode':7,'status':'Some of the campaigns are not found, please refresh and try again later'};
             
             bulkInsertCARCampaigns = [];
             for campaignId in campaigns:
              bulkInsertCARCampaigns.append(CAR_Campaign(car_id=ruleId,campaign_id=campaignId));

             CAR_Campaign.objects.bulk_create(bulkInsertCARCampaigns);

             return {'statusCode':0,'status':'Campaigns have been inserted successfully'};

          except Contextual_Ads_Rule.DoesNotExist as ex:
              return {'statusCode':3,'status':
                  "Invalid request parameters rule not found,"+str(ex)};
          
          except IntegrityError as e:
            return {'statusCode':5,'status':
            "Player has already some of the campaigns provided, please check and add again "};

          except Exception as e:
              return {'statusCode':3,'status':
                  "error "+str(e)};

    def remove(ruleId,userId,campaigns,isWeb):
          if(isWeb == False):
              userId = User_unique_id.getUserId(userId);
              if(userId == False):
                  return {'statusCode':1,'status':
                  "Invalid session, please login"};
          
          try:
             #check for device
             ruleInfo = Contextual_Ads_Rule.objects.get(id=ruleId,iot_device__user_id=userId);
             campaigns = json.loads(campaigns);
                           
             CAR_Campaign.objects.filter(car_id=ruleId,campaign_id__in=campaigns).delete();
             
             return {'statusCode':0,'status':'Campaigns have been removed successfully'};

          except Contextual_Ads_Rule.DoesNotExist as ex:
              return {'statusCode':3,'status':
                  "Invalid request parameters rule not found,"+str(ex)};
          
          
          except Exception as e:
              return {'statusCode':3,'status':
                  "error "+str(e)};

#contextual ads rules associated DSP(signages)
class CAR_Device(models.Model):
    car = models.ForeignKey('iot_device.Contextual_Ads_Rule',on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
    
    class Meta(object):
        unique_together = [
        ['car','player']
        ]

    def assignNew(ruleId,userId,players,isWeb):
          if(isWeb == False):
              userId = User_unique_id.getUserId(userId);
              if(userId == False):
                  return {'statusCode':1,'status':
                  "Invalid session, please login"};
          
          try:
             #check for device
             ruleInfo = Contextual_Ads_Rule.objects.get(id=ruleId,iot_device__user_id=userId);
             players = json.loads(players);
             #check for campaigns
             if(Player.checkForvalidPlayers(players,userId)):
              return {'statusCode':7,'status':'Some of the players are not found, please refresh and try again later'};
             
             bulkInsertCARPlayers = [];
             for playerId in players:
              bulkInsertCARPlayers.append(CAR_Device(car_id=ruleId,player_id=playerId));

             CAR_Device.objects.bulk_create(bulkInsertCARPlayers);

             return {'statusCode':0,'status':'Devices have been assigned successfully'};

          except Contextual_Ads_Rule.DoesNotExist as ex:
              return {'statusCode':3,'status':
                  "Invalid request parameters rule not found,"+str(ex)};
          
          except IntegrityError as e:
            return {'statusCode':5,'status':
            "Player has already some of the devices provided, please check and add again "};

          except Exception as e:
              return {'statusCode':3,'status':
                  "error "+str(e)};

    def remove(ruleId,userId,players,isWeb):
          if(isWeb == False):
              userId = User_unique_id.getUserId(userId);
              if(userId == False):
                  return {'statusCode':1,'status':
                  "Invalid session, please login"};
          
          try:
             #check for device
             ruleInfo = Contextual_Ads_Rule.objects.get(id=ruleId,iot_device__user_id=userId);
             players = json.loads(players);
                           
             CAR_Device.objects.filter(car_id=ruleId,player_id__in=players).delete();
             
             return {'statusCode':0,'status':'Devices have been removed successfully'};

          except Contextual_Ads_Rule.DoesNotExist as ex:
              return {'statusCode':3,'status':
                  "Invalid request parameters rule not found,"+str(ex)};
          
          
          except Exception as e:
              return {'statusCode':3,'status':
                  "error "+str(e)};

    def getAssignedRules(secretKey,isUserId,playerMac):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
      playerInfo = Player.isMyPlayer(playerMac,userId,False);
      if(playerInfo==False):
        return {'statusCode':6,'status':'Invalid player'}
      with connection.cursor() as cursor:
        conditionQuery = '''SELECT rules.*, camInfo.info, campaigns.*  FROM iot_device_car_device as iot_devices 
            INNER JOIN iot_device_contextual_ads_rule as rules ON iot_devices.car_id = rules.id LEFT JOIN 
            iot_device_car_campaign as rule_campaigns ON rules.id = rule_campaigns.car_id INNER JOIN 
            cmsapp_multiple_campaign_upload as campaigns ON rule_campaigns.campaign_id = campaigns.id LEFT JOIN 
            campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE (iot_devices.player_id=%s) 
            group by campaigns.id ORDER BY campaigns.updated_date DESC'''
            
        cursor.execute(conditionQuery,[playerInfo.id])
        rules = dictfetchall(cursor);
        if(len(rules)<=0):
            return {'statusCode':2,'status':
            'No rules Found','conditionQuery':str(conditionQuery)};
        else:
            return {'statusCode':0,'rules':rules};

