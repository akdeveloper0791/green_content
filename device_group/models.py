from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime
from cmsapp.models import User_unique_id,Multiple_campaign_upload
from django.db import IntegrityError
import json
from player.models import Player
from campaign.models import Player_Campaign
from django.db import connection

# Create your models here.
def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
# Create your models here.
class Device_Group(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=False,null=False)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    class Meta(object):
        unique_together = [
        ['user', 'name']
        ]

    def isMyDeviceGroup(dgId,userId):
      try:
        
        deviceGroup = Device_Group.objects.get(id=dgId,
            user_id=userId);
        return deviceGroup;
      except Device_Group.DoesNotExist:
        return False;
    
    def getMyGroups(userId):
      groups = Device_Group.objects.filter(user_id=userId);
      return list(groups.values());

    def createGroup(accessToken,name,isWeb):
        if(isWeb != True):
            accessToken = User_unique_id.getUserId(accessToken);
            
            if(accessToken == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        try:
            group = Device_Group();
            group.user_id = accessToken
            group.name = name
            group.created_date = datetime.datetime.now()
            group.updated_date = datetime.datetime.now()
            group.save()
            return {'statusCode':0,'status':
            'Group has been created successfully'};
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, members should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group already exist with same name, please use different name"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters"+str(e)};

        return {'statusCode':1,'status':
                "Invalid session, please login"}; 
    
    def deleteDG(dgId,accessToken,isWeb):
        if(isWeb != True):
            accessToken = User_unique_id.getUserId(accessToken);  
            if(accessToken == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        try:
            Device_Group.objects.get(id=dgId,user_id=accessToken).delete();
            return {'statusCode':0,'status':'Device Group has been deleted'};
            
        except Device_Group.DoesNotExist:
            return {'statusCode':2,'status':'Device Group not found'};


    def getDGInfo(secretKey,isUserId,dgId,isCampaigns=True,isDevices=True):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login11"};

      try:
        #check for device
        dgInfo = Device_Group.objects.get(id=dgId,user_id=userId);
        info={'id':dgInfo.id,'name':dgInfo.name,
        'created_at':dgInfo.created_date};
        returnJSON = {'statusCode':0,'info':info};
        
        if(isCampaigns==True):
          associatedCampaigns = Device_Group_Campaign.objects.filter(device_group_id=dgId).values('campaign__campaign_name','campaign__id');
          returnJSON['campaigns'] =list(associatedCampaigns);
        
        if(isDevices==True):
          with connection.cursor() as cursor:
            query = '''SELECT player.id,player.name,device_group.id as dg_device_Id FROM player_player as player 
              LEFT JOIN device_group_device_group_player as device_group ON player.id = device_group.player_id AND device_group.device_group_id=%s 
              WHERE (player.user_id=%s)'''
            cursor.execute(query,[dgId,userId]);
            associatedDevices = dictfetchall(cursor);
            returnJSON['devices'] =list(associatedDevices);
        
        return returnJSON;

      except Device_Group.DoesNotExist:
        return {'statusCode':2,'status':'Invalid rule, info not found'}

class Device_Group_Player(models.Model):
    device_group = models.ForeignKey('device_group.Device_Group',on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
    
    class Meta(object):
        unique_together= [
        ['device_group','player']
        ]
    
    def assignNewPlayers(userId,gId,players,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           players =  json.loads(players);
           return Device_Group_Player.addPlayer(userId,gId,players);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the players provided, please check and add again-"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};
    
    def addPlayer(userId,gId,players):
        if(players and len(players)>=1 and gId):
            playerIds = Player.objects.filter(id__in=players);
            
            if(len(playerIds) < len(players)):
                return {'statusCode':4,'status':"Some of the selected players are not valid GC users, you can not add them to groups"};
            
            else:
                try:
                    groupInfo = Device_Group.objects.get(id=gId,user_id=userId);
                    #memberUsers = list(userEmails.values('id'));
                
                    groupPlayers = [];
                    for pId in players:
                      groupPlayer = Device_Group_Player(device_group_id = gId,
                      player_id = pId);
                      groupPlayers.append(groupPlayer);
                    #save group members
                    Device_Group_Player.objects.bulk_create(groupPlayers);
                    #enable in localhost
                    #SendGroupAssignNotifications(members,gId,groupInfo.name,userId).start();
                    #enable in server
                    
                    return {'statusCode':0,"status":
                     "Players have been assigned successfully"};
                except Device_Group.DoesNotExist:
                    return {'statusCode':4,
                    'status':"Group not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};

    def removePlayers(userId,gId,players,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           players =  json.loads(players);
           return Device_Group_Player.checkAndRemovePlayer(userId,gId,players);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the members provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};
    
    def checkAndRemovePlayer(userId,gId,players):
        if(players and len(players)>=1 and gId):
            try:
                groupInfo = Device_Group.objects.get(id=gId,user_id=userId);   
                Device_Group_Player.objects.filter(device_group_id=gId,player_id__in=players).delete();
                return {'statusCode':0,"status":
                     "Players have been removed successfully"};
            except Device_Group.DoesNotExist:
                    return {'statusCode':4,
                    'status':"Group not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};

class Device_Group_Campaign(models.Model):
    device_group = models.ForeignKey('device_group.Device_Group',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    dgc_schedule_type = models.SmallIntegerField(default=10)#10->schedule always
    dgc_priority = models.IntegerField(default=0)
    dgc_is_skip = models.SmallIntegerField(default=0)#0->false, 1->skip true

    class Meta(object):
        unique_together=[
        ['device_group','campaign']
        ]

    def getDGCampaign(dgId,campaignId,userId):
        try:
            info = Device_Group_Campaign.objects.get(
                device_group_id=dgId,campaign_id=campaignId,device_group__user_id=userId);
            return info;
        except Device_Group_Campaign.DoesNotExist:
            return False;

    def assignNewCampaigns(userId,gId,campaigns,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           campaigns =  json.loads(campaigns);
           return Device_Group_Campaign.addCampaign(userId,gId,campaigns);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};


    def addCampaign(userId,gId,campaigns):
        if(gId and int(gId)>=1 and campaigns and len(campaigns)>=1):
            #check group info
            try:
                groupInfo = Device_Group.objects.get(id=gId,user_id=userId);
                
                 #check for campaigns (provided campaigns must be user uploaded)
                if(Player_Campaign.checkForvalidCampaigns(campaigns,userId)):
                    #prepare object to bulk insert
                    groupCampaignsBulk = [];
                    for campaignId in campaigns:
                        groupCampaignsBulk.append(
                            Device_Group_Campaign(device_group_id=gId,campaign_id=campaignId));

                    Device_Group_Campaign.objects.bulk_create(groupCampaignsBulk);
                    
                    return {'statusCode':0,'status':
                    'Campaigns have been assigned successfully'};
                else:
                    return {'statusCode':5,'status':
                    'Some of the campaigns are not found, please refresh and try again later'};
            except Device_Group.DoesNotExist:
                return {'statusCode':4,
                'status':"Group not found please check and try again"};
            return {'campaigns':campaigns};
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};
    
    def removeCampaigns(userId,gId,campaigns,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           campaigns =  json.loads(campaigns);
           return Device_Group_Campaign.checkAndRemoveCampaign(userId,gId,campaigns);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};

    def checkAndRemoveCampaign(userId,gId,campaigns):
        if(gId and int(gId)>=1 and campaigns and len(campaigns)>=1):
            #check group info
            try:
                groupInfo = Device_Group.objects.get(id=gId,user_id=userId);   
                Device_Group_Campaign.objects.filter(device_group_id=gId,campaign_id__in=campaigns).delete()
                return {'statusCode':0,'status':
                    'Campaigns have been removed successfully'};
                
            except Device_Group.DoesNotExist:
                return {'statusCode':4,
                'status':"Group not found please check and try again"};
            return {'campaigns':campaigns};
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};
