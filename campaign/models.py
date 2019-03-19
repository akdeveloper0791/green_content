from django.db import models
from cmsapp.models import Multiple_campaign_upload
import json
from cmsapp.models import User_unique_id
import datetime
from django.db import transaction, connection
from signagecms import constants
import requests 
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from .Notifications import SendCampDeleteNotification,SendEmail
import uuid 
import time
from player.models import Player
from django.db import IntegrityError


def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your models here.
class CampaignInfo(models.Model):
    campaign_id = models.OneToOneField('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE,primary_key=True)
    info = models.TextField()

    def processInfoAndSaveCampaign(info,requestFrom,user_sessionId,
        campaignName,campaignSize=0):
        self = CampaignInfo();
        secretKey = user_sessionId; #upload folder in dropbox
        if(requestFrom == "api"):
            #get the user id from secret key
            userId = User_unique_id.getUserId(user_sessionId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};

        else:
            userId = user_sessionId;
            #get session id to save the 
            secretKey = User_unique_id.getUniqueKey(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        infoObj = json.loads(info);
        if('type' in infoObj):
            if(infoObj['type']=="multi_region"):
                campType = 1#multi region
            else:
                campType = 0#single region
        #savePath = '/campaigns/{}/{}/'.format(secretKey,campaignName);
        uniqueKey = str(uuid.uuid4().hex[:6].upper())+str(round(time.time() * 1000))+uuid.uuid4().hex[:6];
        savePath = '/campaigns/{}/{}/'.format(uniqueKey,campaignName);
        saveInfo = self.createCampaign(userId,campaignName,campType,
            info,campaignSize,savePath);
        
        if(saveInfo['status'] == True):
            
            return {'isSave':True,'statusCode':0,'status':
            "success",'save_path':saveInfo['savePath']}
        else:
            return {'statusCode':3,'status':
            "Unable to upload campaign "+''.join(saveInfo['error'])}
        

    @classmethod
    def createCampaign(cls,userId,name,campType,info,campaignSize,savePath):
        try:
         with transaction.atomic():
            #check for duplicate
            try:
                campaignToSave = Multiple_campaign_upload.objects.get(campaign_uploaded_by=userId,campaign_name=name)
                #if campaign exist get save path from db
                savePath = campaignToSave.save_path;

            except Multiple_campaign_upload.DoesNotExist:
                campaignToSave = Multiple_campaign_upload()
            #campaignToSave = Multiple_campaign_upload()
            campaignToSave.campaign_uploaded_by = userId
            campaignToSave.campaign_name = name
            campaignToSave.created_date = datetime.datetime.now()
            campaignToSave.updated_date = datetime.datetime.now()
            campaignToSave.camp_type = campType
            campaignToSave.stor_location = 2 #indicates drop box
            campaignToSave.campaignSize = campaignSize
            campaignToSave.save_path = savePath
            campaignToSave.save()
            
            #save info file
            try:
                campInfo = CampaignInfo.objects.get(campaign_id_id=campaignToSave.id)
            except CampaignInfo.DoesNotExist:
                campInfo = CampaignInfo()
                campInfo.campaign_id_id = campaignToSave.id
            campInfo.info = info
            campInfo.save()
         return {'status':True,'savePath':savePath}
        except Exception as e:
            
            return {'status':False,'error':e.args}
    
    #get campaigns created by user
    def getUserCampaigns(userId,isUserId=False):
        if(isUserId==False):
            userId = User_unique_id.getUserId(user_sessionId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId).order_by('-updated_date');
        if(len(campaigns)<=0):
            return {'statusCode':2,'status':
            'No campaigns Found'};
        else:
            return {'statusCode':0,'campaigns':list(campaigns.values())};

    def getUserCampaignsWithInfo(userId,isUserId=False):
        if(isUserId==False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT campaigns.*, camInfo.info  FROM cmsapp_multiple_campaign_upload as campaigns 
                LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE (campaigns.campaign_uploaded_by =  %s OR campaigns.id IN ( 
                    SELECT campaign_id FROM campaign_approved_group_campaigns WHERE user_id=%s )) 
                group by campaigns.id ORDER BY campaigns.updated_date DESC'''
            
            cursor.execute(conditionQuery,[userId,userId])
            campaigns = dictfetchall(cursor);
            cursor.close();
            connection.close();
        
        #campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
        if(len(campaigns)<=0):
            return {'statusCode':2,'status':
            'No campaigns Found'};
        else:
            return {'statusCode':0,'campaigns':campaigns};

    def deleteMyCampaign(campaignId,accessToken,mac,isWeb):
        userId=accessToken;
        if(isWeb==False):
            userId = User_unique_id.getUserId(accessToken);
            if(userId == False):
                return {'statusCode':1,'status':
                         "Invalid session, please login"};
        with transaction.atomic():
            #get campaign info
            try:
                campaign = Multiple_campaign_upload.objects.get(id=campaignId,campaign_uploaded_by=userId)
                campaignName = campaign.campaign_name;
                #check and delete campaign from dropbox
                if(campaign.source==0):
                    #deleteCampaignFromDropBox
                    savePath = campaign.save_path;
                    savePath = savePath[:-1]
                    post_data = JsonResponse({ "path": savePath })
                    headers = {'Authorization': 'Bearer {}'.format(constants.DROP_BOX_ACCESS_TOKEN),
                    'Content-Type': 'application/json'}
                    response = requests.post('https://api.dropboxapi.com/2/files/delete_v2', data=post_data,
                     headers=headers);
                
                #delete campaign 
                campaign.delete();

                #save deleted 
                deletedInfo = Deleted_Campaigns(user_id=userId,
                    campaign_name=campaignName,mac=mac);

                deletedInfo.save();

                #send delete confirmation mail
                message = ''' Dear user your campaign {} has been deleted by {}'''.format(campaignName,mac);
                SendCampDeleteNotification(userId, message).start()
                #res = SendEmail.sendEmail(userId,message);
                return {'statusCode':0,'status':'Campaign has been deleted successfully'};
            except Multiple_campaign_upload.DoesNotExist:
                #check whether campaign is assigned or not
                try:
                    campaign = Approved_Group_Campaigns.objects.get(user_id=userId,campaign_id=campaignId);
                    return {'statusCode':2,'status':'Dear  User,  This is Campaign is Shared from Group. Please go to My Memberships in GC Groups and Remove'}
                except:
                    return {'statusCode':2,'status':'Invalid campaign'}
            except Exception as e:
                return {'statusCode':3,'status':'Error -'+str(e)};

        
   
    def listCampaigns1():
    
      with connection.cursor() as cursor:
        
        conditionQuery = '''SELECT campaigns.*,user.username as memberName,uniqueId.user_unique_key  FROM cmsapp_multiple_campaign_upload as campaigns 
                 INNER JOIN auth_user as user on campaigns.campaign_uploaded_by=user.id INNER JOIN cmsapp_user_unique_id as uniqueId on user.id = uniqueId.user_id 
                 WHERE stor_location = 2  order by campaigns.updated_date DESC'''
        cursor.execute(conditionQuery)
        campaigns = dictfetchall(cursor);
        cursor.close();
        connection.close();
        return {'campaigns':campaigns,'total':len(campaigns)}

    def updateSavePath(userId,accessToken):
        campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
        path="no";
        i=0;
        for campaign in campaigns:
            newPath = "/campaigns/{}/{}/".format(accessToken,campaign.campaign_name)
            campaign.save_path = newPath;
            campaign.save();
            i+=1;
           

        return {'path':newPath,'userId':userId,'total':len(campaigns),
        'updated':i};

    def getPreviewCampaignInfo(userId,cId):
        query='''SELECT cInfo.info,campaign.save_path,campaign.campaign_name FROM cmsapp_multiple_campaign_upload as campaign 
        INNER JOIN campaign_campaigninfo as cInfo ON cInfo.campaign_id_id=campaign.id WHERE ((campaign.id=%s AND campaign.campaign_uploaded_by = %s))
        OR campaign.id = (SELECT campaign_id FROM group_groupcampaigns WHERE campaign_id=%s AND gc_group_id IN (SELECT gc_group_id FROM group_gcgroupmembers WHERE member_id = %s) group by campaign_id LIMIT 1)''';
        with connection.cursor() as cursor:
            cursor.execute(query,[cId,userId,cId,userId]);
            info = cursor.fetchone();
            if info == None:
                    return {"statusCode":2,"status":"Invalid details"};
            else:
                    return {"statusCode":0,"cInfo":json.loads(info[0]),"save_path":info[1],'c_name':info[2]};

class Deleted_Campaigns(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=50)
    mac = models.CharField(max_length=50)
    deleted_at = models.DateTimeField(default=datetime.datetime.now())

class Approved_Group_Campaigns(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    group = models.ForeignKey('group.GcGroups',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)
    group_campaign = models.ForeignKey('group.GroupCampaigns',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    class Meta(object):
        unique_together = [
        ['user','campaign','group','group_campaign']
        ]

    def removeApprovedCampaign(userId,recId,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        try:
            approvedCampaign = Approved_Group_Campaigns.objects.get(id=recId,user_id=userId);
            approvedCampaign.delete();
            return {'statusCode':0,'status':'Campaign has been removed successfully'};
        except Approved_Group_Campaigns.DoesNotExist:
            return {'statusCode':3,'status':'Campaign not found'};

class Player_Campaign(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    class Meta(object):
        unique_together = [
        ['user','player','campaign']
        ]
  
    def getCampaignsInfo(userId,playerId,isUserId=False):
        if(isUserId == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        #get group info
        try:
            #playerInfo = Player.objects.get(id=playerId,user_id=userId);
            campaigns = Player_Campaign.objects.filter(campaign__campaign_uploaded_by=userId,player_id=playerId).select_related('campaign');
            campaigns = list(campaigns.values('campaign__id','campaign__campaign_name'));
            return {'statusCode':0,
            'campaigns':campaigns};

        except Player.DoesNotExist:
            return {'statusCode':2,'status':'Player not found'}

    def assignNewCampaigns(userId,pId,campaigns,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           campaigns =  json.loads(campaigns);
           return Player_Campaign.addCampaign(userId,pId,campaigns);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Player has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};

    def addCampaign(userId,pId,campaigns):
        if(pId and int(pId)>=1 and campaigns and len(campaigns)>=1):
            #check group info
            try:
                playerInfo = Player.objects.get(id=pId,user_id=userId);
                #check for campaigns (provided campaigns must be user uploaded)
                multipleCampaigns = Multiple_campaign_upload.objects.filter(
                    id__in=campaigns,campaign_uploaded_by=userId);
                multipleCampaignLength = len(multipleCampaigns);

                if(multipleCampaignLength == len(campaigns)):
                    #prepare object to bulk insert
                    campaignsBulk = [];
                    for campaignId in campaigns:
                        campaignsBulk.append(
                            Player_Campaign(user_id=userId,player_id=pId,campaign_id=campaignId));

                    Player_Campaign.objects.bulk_create(campaignsBulk);
                    
                    return {'statusCode':0,'status':
                    'Campaigns have been assigned successfully'};
                else:
                    return {'statusCode':5,'status':
                    'Some of the campaigns are not found, please refresh and try again later'};
            except Player.DoesNotExist:
                return {'statusCode':4,
                'status':"Player not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};

    def removeCampaigns(userId,pId,campaigns,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           campaigns =  json.loads(campaigns);
           return Player_Campaign.checkAndRemoveCampaign(userId,pId,campaigns);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Player has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};

    def checkAndRemoveCampaign(userId,pId,campaigns):
        if(pId and int(pId)>=1 and campaigns and len(campaigns)>=1):
            #check group info
            try:
                #groupInfo = GcGroups.objects.get(id=gId,user_id=userId);   
                Player_Campaign.objects.filter(user_id=userId,player_id=pId,campaign_id__in=campaigns).delete()
                return {'statusCode':0,'status':
                    'Campaigns have been removed successfully'};
                
            except PLayer.DoesNotExist:
                return {'statusCode':4,
                'status':"Player not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};
    
    def getPlayerCampaignsWithInfo(player,secretKey):
        userId = User_unique_id.getUserId(secretKey);
        if(userId == False):
            return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT campaigns.*, camInfo.info  FROM cmsapp_multiple_campaign_upload as campaigns 
                LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE (campaigns.id IN ( 
                    SELECT campaign_id FROM campaign_player_campaign WHERE user_id=%s and player_id= %s)) 
                group by campaigns.id ORDER BY campaigns.updated_date DESC'''
            
            cursor.execute(conditionQuery,[userId,player])
            campaigns = dictfetchall(cursor);
            cursor.close();
            connection.close();
        
        #campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
        if(len(campaigns)<=0):
            return {'statusCode':2,'status':
            'No campaigns Found'};
        else:
            return {'statusCode':0,'campaigns':campaigns};