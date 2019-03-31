from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime
from cmsapp.models import User_unique_id,Multiple_campaign_upload
from django.db import IntegrityError
import json
from player.models import Player

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

    class Meta(object):
        unique_together=[
        ['device_group','campaign']
        ]
