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

import secrets
class IOT_Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    mac = models.CharField(max_length=125,blank=False,null=False,unique=False,db_index=True)
    key = models.CharField(max_length=125,blank=False,null=False,unique=True,db_index=True,default="adskite")#auto generate
    name = models.CharField(max_length=50,blank=False,null=False)
    device_type = models.CharField(max_length=50,blank=False,null=False)
    registered_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta(object):
        unique_together = [
        ['mac','device_type']
        ]

    def registerPlayer(data,userId,isThirdPlayer=False):
        try:
           data =  json.loads(data);
           uniqueKey = secrets.token_urlsafe(32);
           try:
            player = IOT_Device.objects.get(mac=data['mac'],device_type=data["device_type"])
            if(isThirdPlayer and player.user_id!=userId):
              return {'statusCode':6,'status':'Device has been assigned to different user,cannot assign to you'}
            else:#if not third app then update the user id
              player.user_id = userId;#if th
           except IOT_Device.DoesNotExist:
            player = IOT_Device(mac=data['mac'],key=uniqueKey);
            player.user_id = userId      
           
           
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

    def isMyPlayer(playerKey,userId,isKey=True):
      try:
        if(isKey):
          player = IOT_Device.objects.get(key=playerKey,
            user_id=userId);
        else:
          player = IOT_Device.objects.get(id=playerKey,
            user_id=userId);
        return player;
      except IOT_Device.DoesNotExist:
        return False;
    
    def checkMyPlayers(players,userId,isKey=True):
      try:
        if(isKey):
          player = IOT_Device.objects.filter(key__in=players,
            user_id=userId);
        else:
          player = IOT_Device.objects.get(id__in=players,
            user_id=userId);

        if(len(player) == len(players)):
          return player;
      except IOT_Device.DoesNotExist:
        return False;

    def getPlayer(playerId,playerKey):
      try:
        player = IOT_Device.objects.get(id=playerId,
          key=playerKey);
        return player;
      except IOT_Device.DoesNotExist:
        return False;

    def getPlayer(playerKey):
      try:
        player = IOT_Device.objects.get(key=playerKey);
        return player;
      except IOT_Device.DoesNotExist:
        return False;

    def getContextualAdRules(secretKey,isUserId,playerKey):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login11"};
      
      playerInfo1=None;
      if(playerKey=="1"):
        rules = Contextual_Ads_Rule.objects.filter(iot_device__user_id = userId);
      else:
        playerInfo = IOT_Device.isMyPlayer(playerKey,userId);
        if(playerInfo==False):
          return {'statusCode':6,'status':'Invalid player'}
        
        playerInfo1={'type':playerInfo.device_type};

        rules = Contextual_Ads_Rule.objects.filter(iot_device = playerInfo);
      if(len(rules)>=1):
        return {'statusCode':0,'rules':list(rules.values('id','iot_device_id',
          'classifier','delay_time','created_at','accessed_at','iot_device__name','iot_device__device_type')),'playerInfo':playerInfo1};
      else:
        return {'statusCode':2,'status':'No rules found','playerInfo':playerInfo1};

    def getIOTDevicesCARules(secretKey,isUserId,players):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login11"};
      
      try:
        players = json.loads(players);
        playerInfo = IOT_Device.checkMyPlayers(players,userId);
        if(playerInfo==False):
          return {'statusCode':6,'status':'Invalid player'}
         
        playerIds = [playerId for playerId in playerInfo.values_list('id')][0];
        
        with connection.cursor() as cursor:
          query = '''SELECT car.*,carGps.classifier_lat,carGps.classifier_lng FROM  iot_device_contextual_ads_rule as car LEFT JOIN 
          iot_device_gps_car_data as carGPS ON carGPS.car_id = car.id WHERE 
          car.iot_device_id IN ({}) '''.format(','.join(['%s' for _ in range(len(playerIds))])) 
          cursor.execute(query,playerIds);
          rules = dictfetchall(cursor);
          if(len(rules)>=1):
            return {'statusCode':0,'rules':rules};
          else:
            return {'statusCode':2,'status':'No rules found'};
      except ValueError:
        return {'statusCode':7,'status':'Invalid players'};

      
    
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
  
from django.db.models import Count
class Contextual_Ads_Rule(models.Model):
    iot_device = models.ForeignKey('iot_device.IOT_Device',on_delete=models.CASCADE)
    classifier = models.CharField(max_length=125,blank=False,null=False,db_index=True)
    delay_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    accessed_at = models.DateTimeField(null=True)
    def createRule(iotDeviceKey,userId,players,campaigns,calssifier,delayTime,gpsCARData,isWeb):
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
                
                if(len(players)>=1):
                  bulkInsertCARPlayers = [];
                  for playerId in players:
                    bulkInsertCARPlayers.append(CAR_Device(car_id=ca_rule.id,player_id=playerId));

                  CAR_Device.objects.bulk_create(bulkInsertCARPlayers);
                
                if(gpsCARData != "false"):
                  gpsCARData = json.loads(gpsCARData);
                  gpsCarDataObj = GPS_CAR_Data(car_id=ca_rule.id,
                    classifier_lat=gpsCARData['classifier_lat'],classifier_lng=gpsCARData['classifier_lng']);
                  gpsCarDataObj.save();

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
    
    def updateAccessAt(classifiers):
      if(len(classifiers)>=1):
        Contextual_Ads_Rule.objects.filter(id__in=classifiers).update(accessed_at=timezone.now());
        return True;
      return False;

    def listMicPhoneClassifiers(userId):
      #classifiers = Contextual_Ads_Rule.objects.filter(
      #  iot_device__user_id=userId,iot_device__device_type="Microphone").values('classifier');
      classifiers = Contextual_Ads_Rule.objects.values('classifier').annotate(
        name_count=Count('classifier')).filter(iot_device__user_id=userId,iot_device__device_type="Microphone").values('classifier');
      return {"statusCode":0,"classifiers":list(classifiers)};
    
    def broadcastRulesByClassiferNames(playerKey,classifiers,players=False,deviceMac=False):
      ''' player key is the iot device key 
          and players are DSP's which you want to push the classifers(optional)'''
      try:
        classifiers = json.loads(classifiers);
        lowerClassifiers = lambda classifier: classifier.lower();
        classifiers = list(map(lowerClassifiers,classifiers));
        
        #publish rules
        return CAR_Device.publishMicPhoneRule(playerKey,json.dumps(classifiers,ensure_ascii=False),
          players,deviceMac);

      except ValueError:
        return {'statusCode':2,'status':'Invalid classifier list'}

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

from pyfcm import FCMNotification
import datetime
from signagecms import constants

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
        conditionQuery = '''SELECT rules.id as rule_id,rules.classifier,rules.delay_time, campaigns.campaign_name,rule_campaigns.id as rc_id  FROM iot_device_car_device as iot_devices 
            INNER JOIN iot_device_contextual_ads_rule as rules ON iot_devices.car_id = rules.id INNER JOIN 
            iot_device_car_campaign as rule_campaigns ON rules.id = rule_campaigns.car_id INNER JOIN 
            cmsapp_multiple_campaign_upload as campaigns ON rule_campaigns.campaign_id = campaigns.id WHERE (iot_devices.player_id=%s) 
            '''
            
        cursor.execute(conditionQuery,[playerInfo.id])
        rules = dictfetchall(cursor);
        if(len(rules)<=0):
            return {'statusCode':2,'status':
            'No rules Found'};
        else:
            return {'statusCode':0,'rules':rules};

    def getDevicesToPublishRule(rule,player):
      devices = CAR_Device.objects.exclude(
        player__fcm_id='null').exclude(
        player__fcm_id__isnull=True).filter(
        car__classifier=rule,car__iot_device__id=player).values(
        'player_id','player__name','player__fcm_id','player__mac','car__delay_time','car');
      return list(devices);
    
    

    def publishRule(playerMac,rule,player):
      devicesToPublish = CAR_Device.getDevicesToPublishRule(rule,player);
      if(len(devicesToPublish)>=1):
        #prepare device to publish
        response = {'includeThis':False,'devicesToPublish':devicesToPublish};
        #return response;
        deviceFcmRegIds = [];
        deviceFcmRegIdsWithInfo={};
        classifiersList = [];
        for device in devicesToPublish:
          classifiersList.append(device['car']);
          if(device['player__mac']==playerMac):
            response['includeThis']=True;
            response['device'] = device;
          else:
            deviceDelay = device['car__delay_time'];
            if(deviceDelay in deviceFcmRegIdsWithInfo):
              deviceInfo = deviceFcmRegIdsWithInfo[deviceDelay];
              deviceFcmRegIds = deviceInfo['deviceFcmRegIds'];
              deviceFcmRegIds.append(device['player__fcm_id']);
              
              
            else:
              deviceFcmRegIdsWithInfo[deviceDelay]={'deviceFcmRegIds':[device['player__fcm_id']]}
            #deviceFcmRegIds.append(device['player__fcm_id']);
        response['deviceFcmRegIdsWithInfo']=deviceFcmRegIdsWithInfo;
        
        push_service = FCMNotification(api_key=constants.fcm_api_key)
        for delayTime,deviceWithInfo in deviceFcmRegIdsWithInfo.items():
          data_message = {
          "action":constants.fcm_handle_metrics_rule,
          "rule":rule,
          "delay_time":delayTime,
          "push_time":str(datetime.datetime.now())
          }
          deviceFcmRegIds = deviceWithInfo['deviceFcmRegIds'];
          if(len(deviceFcmRegIds)>=1):
            if(len(deviceFcmRegIds)==1):
              fcm_result = push_service.notify_single_device(registration_id=deviceFcmRegIds[0],data_message=data_message)
              response['fcm_result'+str(delayTime)] = fcm_result;
            else:
              fcm_result = push_service.notify_multiple_devices(registration_ids=deviceFcmRegIds,data_message=data_message)
              response['fcm_result'+str(delayTime)] = fcm_result;
        
        #fcm_result = push_service.notify_single_device(registration_id='fPauOP7j_Mw:APA91bFsez98VG5EVXgiqXkrpZKwb3mYmhfGyqfj2YuMQ3esOZvIW_LoGr0eHhkjKoJKdok6ARXXfg9uryX53ryn6o2BkVZQozgjSTv5dLcrR5D8lZ23byUrn3qQTxME54pzhHPo5Itc',data_message=data_message)
        #response['fcm_Result']=fcm_result;
        #update classifiers last notified time
        response['classifiersList'] = classifiersList;
        Contextual_Ads_Rule.updateAccessAt(classifiersList);
        return response;
      else:
        return False;

    def getDevicesToPublishMicPhoneRule(rule,iotDeviceKey,players=False):
        
        try:
          players=json.loads(players);
          if(len(players)<=0):
            players=False;
        except Exception as ex:
            players=False;

        if(players==False):
          devices = CAR_Device.objects.exclude(
            player__fcm_id='null').exclude(
            player__fcm_id__isnull=True).filter(
            car__classifier__in=rule,car__iot_device__key=iotDeviceKey).values(
            'player_id','player__name','player__fcm_id','player__mac','car__delay_time','car');
        else:
          devices=CAR_Device.objects.exclude(
          player__fcm_id='null').exclude(
          player__fcm_id__isnull=True).filter(
          player__mac__in=players,car__classifier__in=rule,car__iot_device__key=iotDeviceKey).values(
          'player_id','player__name','player__fcm_id','player__mac','car__delay_time','car');
        return list(devices);
    
    
    
    def publishMicPhoneRule(player,rule,players=False,playerMac=False):

      try:
        if(playerMac==False):
          playerInfo = IOT_Device.getPlayer(player);
          if(playerInfo==False):
            return {'statusCode':2,'status':'Invalid device'};
          playerMac  = playerInfo.mac     
        rule = json.loads(rule);
        devicesToPublish = CAR_Device.getDevicesToPublishMicPhoneRule(rule,player,players);
        if(len(devicesToPublish)>=1):
          #prepare device to publish
          response = {'statusCode':0,'includeThis':False};
          #response['devicesToPublish'] = devicesToPublish;
          #return response;
          deviceFcmRegIds = [];
          deviceFcmRegIdsWithInfo={};
          duplicateDevice=[];
          classifiersList = [];
          for device in devicesToPublish:
            deviceFCM = device['player__fcm_id'];
            classifiersList.append(device['car']);
            if(device['player__mac']==playerMac):
              response['includeThis']=True;
              response['delay_time'] = device['car__delay_time'];
              response['rule'] = json.dumps(rule);
            else:
              if deviceFCM not in duplicateDevice:
                duplicateDevice.append(deviceFCM);
                deviceDelay = device['car__delay_time'];
                if(deviceDelay in deviceFcmRegIdsWithInfo):
                  deviceInfo = deviceFcmRegIdsWithInfo[deviceDelay];
                  deviceFcmRegIds = deviceInfo['deviceFcmRegIds'];
                  deviceFcmRegIds.append(deviceFCM);      
                else:
                  deviceFcmRegIdsWithInfo[deviceDelay]={'deviceFcmRegIds':[deviceFCM]}
              #deviceFcmRegIds.append(device['player__fcm_id']);
          #response['deviceFcmRegIdsWithInfo']=deviceFcmRegIdsWithInfo;
          
          push_service = FCMNotification(api_key=constants.fcm_api_key)
          for delayTime,deviceWithInfo in deviceFcmRegIdsWithInfo.items():
            
            data_message = {
            "action":constants.fcm_handle_mic_rule,
            "rule":json.dumps(rule),
            "delay_time":delayTime,
            "push_time":str(datetime.datetime.now())
            }

            deviceFcmRegIds = deviceWithInfo['deviceFcmRegIds'];
            if(len(deviceFcmRegIds)>=1):
              if(len(deviceFcmRegIds)==1):
                fcm_result = push_service.notify_single_device(registration_id=deviceFcmRegIds[0],data_message=data_message)
                #response['fcm_result'+str(delayTime)] = fcm_result;
              else:
                fcm_result = push_service.notify_multiple_devices(registration_ids=deviceFcmRegIds,data_message=data_message)
                #response['fcm_result'+str(delayTime)] = fcm_result;
          
          #fcm_result = push_service.notify_single_device(registration_id='fPauOP7j_Mw:APA91bFsez98VG5EVXgiqXkrpZKwb3mYmhfGyqfj2YuMQ3esOZvIW_LoGr0eHhkjKoJKdok6ARXXfg9uryX53ryn6o2BkVZQozgjSTv5dLcrR5D8lZ23byUrn3qQTxME54pzhHPo5Itc',data_message=data_message)
          #response['fcm_Result']=fcm_result;
          #response['classifiersList'] = classifiersList;
          #update classifiers last notified time
          Contextual_Ads_Rule.updateAccessAt(classifiersList);
          return response;
        else:
          return {'statusCode':6,'status':'No devices to publish'};
      except ValueError as ex:
        return {'statusCode':6,'status':'Invalid classifier'+str(ex)};

from django.db.models import Sum
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

  def saveMetrics(player,genders,ages,m_f_ages):
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
        Geder_Age_Metrics.saveMetrics(player,m_f_ages)
        return {'statusCode':0}
      else:
        return {'statusCode':1,'status':"Unable to save metrics"};
    except Exception as ex:
      return {'statusCode':1,'status':"Unable to save metrics - "+str(ex)};

  def getViewerMetrics(secretKey,isUserId,postParams,exportExcel=False):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
      # check for player
      player = postParams.get('player');
      metrics={};
      if(player=="All"):
        #list all metrics
        metrics = Age_Geder_Metrics.objects.filter(iot_device__user_id=userId,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).select_related('iot_device').order_by('-created_at');
      
      elif(IOT_Device.isMyPlayer(player,userId,False)!=False):
        metrics = Age_Geder_Metrics.objects.filter(iot_device_id=player,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).order_by('-created_at');

      if(metrics.exists()):
          if(exportExcel==False):
            return {'statusCode':0,'metrics':list(metrics.values('created_at','g_female','g_male','iot_device__name','age_0_2','age_4_6','age_8_12',
              'age_15_20','age_25_32','age_38_43','age_48_53','age_60_100'))}
          else:
            return {'statusCode':0,'metrics':(metrics.values_list('iot_device__name','created_at','g_male','g_female','age_0_2','age_4_6','age_8_12',
              'age_15_20','age_25_32','age_38_43','age_48_53','age_60_100'))}
      else:
          return {'statusCode':4,'status':"No metrics found for the selected dates"};


  def getViewerBarMetrics(userId,postParams):
      # check for player
      player = postParams.get('player');
      metrics={};
      if(player=="All"):
        #list all metrics
        metrics = Age_Geder_Metrics.objects.filter(iot_device__user_id=userId,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).aggregate(
          Sum('age_0_2'),Sum('age_4_6'),Sum('age_8_12'),Sum('age_15_20'),
          Sum('age_25_32'),Sum('age_38_43'),Sum('age_48_53'),
          Sum('age_60_100'))
      
      elif(IOT_Device.isMyPlayer(player,userId,False)!=False):
        metrics = Age_Geder_Metrics.objects.filter(iot_device_id=player,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).aggregate(
          Sum('age_0_2'),Sum('age_4_6'),Sum('age_8_12'),Sum('age_15_20'),
          Sum('age_25_32'),Sum('age_38_43'),Sum('age_48_53'),
          Sum('age_60_100'))
      #return {'metrics':metrics};
      if(metrics['age_0_2__sum'] == None):
        return {'statusCode':4,'status':"No metrics found for the selected dates"};
      else:
         #prepare metrics
         total=0;
         for key,value in metrics.items():
          total += value;
         labels = ["0-15","15-24","25-37","38-47","48-60","60+"];
         data = [(metrics['age_0_2__sum']+metrics['age_4_6__sum']+metrics['age_8_12__sum']),metrics['age_15_20__sum'],metrics['age_25_32__sum'],
            metrics['age_38_43__sum'],metrics['age_48_53__sum'],metrics['age_60_100__sum']];
         return {'statusCode':0,'metrics':metrics,'total':total,'data':data,'labels':labels} 
      
  def vmGenderPieReports(userId,postParams):
      # check for player
      player = postParams.get('player');
      metrics={};
      if(player=="All"):
        #list all metrics
        metrics = Age_Geder_Metrics.objects.filter(iot_device__user_id=userId,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).aggregate(
          Sum('g_male'),Sum('g_female'))
      
      elif(IOT_Device.isMyPlayer(player,userId,False)!=False):
        metrics = Age_Geder_Metrics.objects.filter(iot_device_id=player,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).aggregate(
          Sum('g_male'),Sum('g_female'))
      #return {'metrics':metrics};
      if(metrics['g_male__sum'] == None):
        return {'statusCode':4,'status':"No metrics found for the selected dates"};
      else:
         #prepare metrics
         total=0;
         for key,value in metrics.items():
          total += value;
         labels = ["Female","Male"];
         data = [metrics['g_female__sum'],metrics['g_male__sum']];
         return {'statusCode':0,'metrics':metrics,'total':total,'data':data,'labels':labels}

import pytz
from dateutil import tz
class Geder_Age_Metrics(models.Model):
  iot_device = models.ForeignKey('iot_device.IOT_Device',on_delete=models.CASCADE,db_index=True)
  created_at = models.DateTimeField(default=timezone.now,blank=False,null=False)
  f_age_0_2 = models.IntegerField(default=0)
  f_age_4_6 = models.IntegerField(default=0)
  f_age_8_12 = models.IntegerField(default=0)
  f_age_15_20 = models.IntegerField(default=0)
  f_age_25_32 = models.IntegerField(default=0)
  f_age_38_43 = models.IntegerField(default=0)
  f_age_48_53 = models.IntegerField(default=0)
  f_age_60_100 = models.IntegerField(default=0)
  m_age_0_2 = models.IntegerField(default=0)
  m_age_4_6 = models.IntegerField(default=0)
  m_age_8_12 = models.IntegerField(default=0)
  m_age_15_20 = models.IntegerField(default=0)
  m_age_25_32 = models.IntegerField(default=0)
  m_age_38_43 = models.IntegerField(default=0)
  m_age_48_53 = models.IntegerField(default=0)
  m_age_60_100 = models.IntegerField(default=0)

  def saveMetrics(device,m_f_ages):
    metrics = Geder_Age_Metrics(iot_device_id=device);
    metrics.f_age_0_2 = m_f_ages[0,0]
    metrics.f_age_4_6 = m_f_ages[0,1]
    metrics.f_age_8_12 = m_f_ages[0,2]
    metrics.f_age_15_20 = m_f_ages[0,3]
    metrics.f_age_25_32 = m_f_ages[0,4]
    metrics.f_age_38_43 = m_f_ages[0,5]
    metrics.f_age_48_53 = m_f_ages[0,6]
    metrics.f_age_60_100 = m_f_ages[0,7]
    metrics.m_age_0_2 = m_f_ages[1,0]
    metrics.m_age_4_6 = m_f_ages[1,1]
    metrics.m_age_8_12 = m_f_ages[1,2]
    metrics.m_age_15_20 = m_f_ages[1,3]
    metrics.m_age_25_32 = m_f_ages[1,4]
    metrics.m_age_38_43 = m_f_ages[1,5]
    metrics.m_age_48_53 = m_f_ages[1,6]
    metrics.m_age_60_100 = m_f_ages[1,7]
    metrics.save();
    return False;

  def vmGenderAgeBarReports(userId,postParams):
      # check for player
      player = postParams.get('player');
      metrics={};
      if(player=="All"):
        #list all metrics
        metrics = Geder_Age_Metrics.objects.filter(iot_device__user_id=userId,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).aggregate(
          Sum('f_age_0_2'),Sum('f_age_4_6'),Sum('f_age_8_12'),Sum('f_age_15_20'),
          Sum('f_age_25_32'),Sum('f_age_38_43'),Sum('f_age_48_53'),
          Sum('f_age_60_100'),Sum('m_age_0_2'),Sum('m_age_4_6'),Sum('m_age_8_12'),Sum('m_age_15_20'),
          Sum('m_age_25_32'),Sum('m_age_38_43'),Sum('m_age_48_53'),
          Sum('m_age_60_100'))
      
      elif(IOT_Device.isMyPlayer(player,userId,False)!=False):
        metrics = Geder_Age_Metrics.objects.filter(iot_device_id=player,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).aggregate(
          Sum('f_age_0_2'),Sum('f_age_4_6'),Sum('f_age_8_12'),Sum('f_age_15_20'),
          Sum('f_age_25_32'),Sum('f_age_38_43'),Sum('f_age_48_53'),
          Sum('f_age_60_100'),Sum('m_age_0_2'),Sum('m_age_4_6'),Sum('m_age_8_12'),Sum('m_age_15_20'),
          Sum('m_age_25_32'),Sum('m_age_38_43'),Sum('m_age_48_53'),
          Sum('m_age_60_100'))
      #return {'metrics':metrics};
      if(metrics['f_age_0_2__sum'] == None):
        return {'statusCode':4,'status':"No metrics found for the selected dates"};
      else:
         #prepare metrics
         
         labels = ["0-15","15-24","25-37","38-47","48-60","60+"];
         f_data = [(metrics['f_age_0_2__sum']+metrics['f_age_4_6__sum']+metrics['f_age_8_12__sum']),metrics['f_age_15_20__sum'],metrics['f_age_25_32__sum'],
            metrics['f_age_38_43__sum'],metrics['f_age_48_53__sum'],metrics['f_age_60_100__sum']];

         m_data = [(metrics['m_age_0_2__sum']+metrics['m_age_4_6__sum']+metrics['m_age_8_12__sum']),metrics['m_age_15_20__sum'],metrics['m_age_25_32__sum'],
            metrics['m_age_38_43__sum'],metrics['m_age_48_53__sum'],metrics['m_age_60_100__sum']];
        
         return {'statusCode':0,'metrics':metrics,'f_data':f_data,'labels':labels,'m_data':m_data} 

  def vmGenderLineReports(userId,postParams):
      # check for player    
      player = postParams.get('player');
      metrics={};
      scheduleFrom = postParams.get('from_date');
      scheduleTo = postParams.get('to_date');

      scheduleFrom = datetime.datetime.strptime(scheduleFrom,"%Y-%m-%d %H:%M:%S")
      scheduleFrom = scheduleFrom.astimezone(pytz.UTC);
      
      scheduleTo = datetime.datetime.strptime(scheduleTo,"%Y-%m-%d %H:%M:%S")
      scheduleTo = scheduleTo.astimezone(pytz.UTC);
      
      if(player=="All"):
        #list all metrics
        with connection.cursor() as cursor:
          query = '''SELECT sum(f_age_0_2+f_age_4_6+f_age_8_12+f_age_15_20+f_age_25_32+f_age_38_43+f_age_48_53+f_age_60_100) as f_graph,
          sum(m_age_0_2+m_age_4_6+m_age_8_12+m_age_15_20+m_age_25_32+m_age_38_43+m_age_48_53+m_age_60_100) as m_graph,strftime(%s, created_at) as time_graph FROM iot_device_geder_age_metrics 
          WHERE iot_device_id IN (SELECT id FROM iot_device_iot_device WHERE user_id=%s)  AND (created_at between %s AND %s ) group by time_graph'''
          cursor.execute(query,['%d-%m-%Y %H',userId,scheduleFrom,scheduleTo])
          metrics = dictfetchall(cursor);
          
  
      elif(IOT_Device.isMyPlayer(player,userId,False)!=False):
        with connection.cursor() as cursor:
          query='''SELECT sum(f_age_0_2+f_age_4_6+f_age_8_12+f_age_15_20+f_age_25_32+f_age_38_43+f_age_48_53+f_age_60_100) as f_graph,
          sum(m_age_0_2+m_age_4_6+m_age_8_12+m_age_15_20+m_age_25_32+m_age_38_43+m_age_48_53+m_age_60_100) as m_graph,strftime(%s, created_at) as time_graph FROM iot_device_geder_age_metrics 
          WHERE iot_device_id = %s  AND (created_at between %s AND %s ) group by time_graph'''
          cursor.execute(query,['%d-%m-%Y %H',player,scheduleFrom,scheduleTo])
          metrics = dictfetchall(cursor);
          
      if(len(metrics)>=1):
        labels = [];mGraph=[];fGraph=[];
        for info in metrics:
          createdDateTime = info['time_graph']+str(":00:00");
          to_zone = tz.gettz('Asia/Kolkata')
          utc = datetime.datetime.strptime(createdDateTime, '%d-%m-%Y %H:%M:%S')
          
          labels.append(utc.astimezone(to_zone))
          
          mGraph.append(info['m_graph']);
          fGraph.append(info['f_graph']);

        return {'statusCode':0,'metrics':metrics,'labels':labels,'f_graph':fGraph,'m_graph':mGraph};
      else:
        return {'statusCode':2,'status':'No Metrics found for the selected dates'};

class GPS_CAR_Data(models.Model):
  car = models.OneToOneField('iot_device.Contextual_Ads_Rule',on_delete=models.CASCADE,unique=True)
  classifier_lat = models.DecimalField(decimal_places=8,max_digits=10)
  classifier_lng = models.DecimalField(decimal_places=8,max_digits=11)