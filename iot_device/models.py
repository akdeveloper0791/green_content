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

    def getPlayer(playerId,playerKey):
      try:
        player = IOT_Device.objects.get(id=playerId,
          key=playerKey);
        return player.id;
      except IOT_Device.DoesNotExist:
        return False;

    def getContextualAdRules(secretKey,isUserId,playerKey):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login11"};
      playerInfo = IOT_Device.isMyPlayer(playerKey,userId);
      if(playerInfo==False):
        return {'statusCode':6,'status':'Invalid player'}
      
      rules = Contextual_Ads_Rule.objects.filter(iot_device = playerInfo).values();
      if(len(rules)>=1):
        return {'statusCode':0,'rules':list(rules)};
      else:
        return {'statusCode':2,'status':'No rules found'};
    
    def getContextualAdRuleInfo(secretKey,isUserId,ruleId,isCampaigns=True,isDevices=True):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login11"};

      try:
        #check for device
        ruleInfo = Contextual_Ads_Rule.objects.get(id=ruleId,iot_device__user_id=userId);
        info={'id':ruleInfo.id,'classifier':ruleInfo.classifier,
        'delay_time':ruleInfo.delay_time,'created_at':ruleInfo.created_at};
        returnJSON = {'statusCode':0,'rule':info};
        
        if(isCampaigns==True):
          associatedCampaigns = CAR_Campaign.objects.filter(car_id=ruleInfo.id).values('campaign__campaign_name','campaign__id');
          returnJSON['campaigns'] =list(associatedCampaigns);
        
        if(isDevices==True):
          with connection.cursor() as cursor:
            query = '''SELECT player.id,player.name,car_device.id as car_device_Id FROM player_player as player 
              LEFT JOIN iot_device_car_device as car_device ON player.id = car_device.player_id AND car_device.car_id=%s 
              WHERE (player.user_id=%s)'''
            cursor.execute(query,[ruleInfo.id,userId]);
            associatedDevices = dictfetchall(cursor);
            returnJSON['devices'] =list(associatedDevices);
        
        return returnJSON;

      except Contextual_Ads_Rule.DoesNotExist:
        return {'statusCode':2,'status':'Invalid rule, info not found'}


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

           return {'statusCode':0,'status':'Rule has been created','id':ca_rule.id};
           
           
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
        conditionQuery = '''SELECT rules.id as rule_id,rules.classifier,rules.delay_time, camInfo.info, campaigns.*  FROM iot_device_car_device as iot_devices 
            INNER JOIN iot_device_contextual_ads_rule as rules ON iot_devices.car_id = rules.id INNER JOIN 
            iot_device_car_campaign as rule_campaigns ON rules.id = rule_campaigns.car_id INNER JOIN 
            cmsapp_multiple_campaign_upload as campaigns ON rule_campaigns.campaign_id = campaigns.id LEFT JOIN 
            campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE (iot_devices.player_id=%s) 
            group by campaigns.id ORDER BY campaigns.updated_date DESC'''
            
        cursor.execute(conditionQuery,[playerInfo.id])
        rules = dictfetchall(cursor);
        if(len(rules)<=0):
            return {'statusCode':2,'status':
            'No rules Found'};
        else:
            return {'statusCode':0,'rules':rules};

class Age_Geder_Metrics(models.Model):
  iot_device = models.ForeignKey('iot_device.IOT_Device',on_delete=models.CASCADE,db_index=True)
  created_at = models.DateTimeField(default=timezone.now,blank=False,null=False)
  g_male=models.IntegerField(default=0)
  g_female=models.IntegerField(default=0)
  age_0_2 = models.IntegerField(default=0)
  age_4_6 = models.IntegerField(default=0)
  age_8_12 = models.IntegerField(default=0)
  age_15_20 = models.IntegerField(default=0)
  age_25_32 = models.IntegerField(default=0)
  age_38_43 = models.IntegerField(default=0)
  age_48_53 = models.IntegerField(default=0)
  age_60_100 = models.IntegerField(default=0)

  def saveMetrics(player,genders,ages):
    try:
      metrics = Age_Geder_Metrics(iot_device_id=player);
      #save gender metrics
      if "Female" in genders:
        metrics.g_female = genders['Female'];
      if "Male" in genders:
        metrics.g_male = genders['Male']

      #age metrics 
      for age in ages:
        if age == "0":
          metrics.age_0_2 = ages[age];
        elif age == "1":
          metrics.age_4_6 = ages[age];
        elif age == "2":
          metrics.age_8_12 = ages[age];
        elif age == "3":
          metrics.age_15_20 = ages[age];
        elif age == "4":
          metrics.age_25_32 = ages[age];
        elif age == "5":
          metrics.age_38_43 = ages[age];
        elif age == "6":
          metrics.age_48_53 = ages[age];
        elif age == "7":
          metrics.age_60_100 = ages[age];
     
      
      metrics.save();
      if(metrics.id>=1):
        return {'statusCode':0}
      else:
        return {'statusCode':1,'status':"Unable to save metrics"};
    except Exception as ex:
      return {'statusCode':1,'status':"Unable to save metrics - "+str(ex)};