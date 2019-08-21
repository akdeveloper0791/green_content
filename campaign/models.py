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
from django.utils import timezone
import os
import shutil
import pytz
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User

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
        campaignName,campaignSize=0,storeLocation=2,userEmailId=False):
        self = CampaignInfo();
        secretKey = user_sessionId; #upload folder in dropbox
        if(requestFrom == "api"):
            #get the user id from secret key
            userId = User_unique_id.getUserId(user_sessionId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
            userEmailId = User.objects.get(id=userId).email;
        else:
            userId = user_sessionId;
            #get session id to save the 
            secretKey = User_unique_id.getUniqueKey(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        try:
            infoObj = json.loads(info);
        except Exception as ex:
            return {'statusCode':6,'status':'Error in processing info json'};

        if('type' in infoObj):
            if(infoObj['type']=="multi_region"):
                campType = 1#multi region
            elif(infoObj['type']=="rss"):
                campType = 2 #rss feed
            else:
                campType = 0#single region
        #savePath = '/campaigns/{}/{}/'.format(secretKey,campaignName);
        uniqueKey = str(uuid.uuid4().hex[:6].upper())+str(round(time.time() * 1000))+uuid.uuid4().hex[:6];
        savePath = '/campaigns/{}/{}/{}/'.format(userEmailId,uniqueKey,campaignName);
        saveInfo = self.createCampaign(userId,campaignName,campType,
            info,campaignSize,savePath,storeLocation);
        
        if(saveInfo['status'] == True):
            return {'isSave':True,'statusCode':0,'status':
            "success",'save_path':saveInfo['savePath'],'cId':saveInfo['id']}
        else:
            return {'statusCode':3,'status':
            "Unable to upload campaign "+''.join(saveInfo['error'])}
        
    @classmethod
    def createCampaign(cls,userId,name,campType,info,campaignSize,savePath,
        storeLocation):
        try:
         with transaction.atomic():
            #check for duplicate
            try:
                campaignToSave = Multiple_campaign_upload.objects.get(campaign_uploaded_by=userId,campaign_name=name)
                #if campaign exist get save path from db
                savePath = campaignToSave.save_path;
                
            except Multiple_campaign_upload.DoesNotExist:
                campaignToSave = Multiple_campaign_upload()
                campaignToSave.stor_location = storeLocation #indicates drop box
                campaignToSave.created_date = timezone.now()
            #campaignToSave = Multiple_campaign_upload()
            campaignToSave.campaign_uploaded_by = userId
            campaignToSave.campaign_name = name
            campaignToSave.updated_date = timezone.now()
            campaignToSave.camp_type = campType
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

         return {'status':True,'savePath':savePath,'id':campaignToSave.id}
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
    
    def getCampaignsToDisplayInWeb(userId):
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT campaigns.*,datetime(campaigns.updated_date,'localtime') as updated_date FROM cmsapp_multiple_campaign_upload as campaigns 
                WHERE (campaigns.campaign_uploaded_by =  %s OR campaigns.id IN ( 
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
    
    import shutil
    import signagecms.constants;
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
                    savePath = savePath.replace(campaign.campaign_name,"");
                    savePath = savePath[:-1]
                    storeLocation = campaign.stor_location;
                    if(storeLocation==2):#drop box
                        post_data = JsonResponse({ "path": savePath })
                        headers = {'Authorization': 'Bearer {}'.format(constants.DROP_BOX_ACCESS_TOKEN),
                        'Content-Type': 'application/json'}
                        response = requests.post('https://api.dropboxapi.com/2/files/delete_v2', data=post_data,
                         headers=headers);
                    elif(storeLocation==1):#local
                        #delete from local storage
                        campaignPath = str(constants.file_storage_path)+savePath;
                        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        if(os.path.exists(os.path.join(BASE_DIR,"media"+savePath))):
                            shutil.rmtree(campaignPath);
                                 
                        
                        
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

    def canUploadCampaignResource(accessToken,campaignId,isWeb):
        userId=accessToken;
        if(isWeb==False):
            userId = User_unique_id.getUserId(accessToken);
            if(userId == False):
                return {'statusCode':1,'status':
                         "Invalid session, please login"};

        try:
            campaign = Multiple_campaign_upload.objects.get(id=campaignId,campaign_uploaded_by=userId);
            return {'statusCode':0,'campaign':campaign};
        except Multiple_campaign_upload.DoesNotExist:
           return {'statusCode':1,'status':'No campaign found'}; 

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
        query='''SELECT cInfo.info,campaign.save_path,campaign.campaign_name,campaign.stor_location,campaign.id as cId FROM cmsapp_multiple_campaign_upload as campaign 
        INNER JOIN campaign_campaigninfo as cInfo ON cInfo.campaign_id_id=campaign.id WHERE ((campaign.id=%s AND campaign.campaign_uploaded_by = %s))
        OR campaign.id = (SELECT campaign_id FROM group_groupcampaigns WHERE campaign_id=%s AND gc_group_id IN (SELECT gc_group_id FROM group_gcgroupmembers WHERE member_id = %s) group by campaign_id LIMIT 1)''';
        with connection.cursor() as cursor:
            cursor.execute(query,[cId,userId,cId,userId]);
            info = cursor.fetchone();
            if info == None:
                    return {"statusCode":2,"status":"Invalid details"};
            else:
                    return {"statusCode":0,"cInfo":json.loads(info[0]),"save_path":info[1],'c_name':info[2],'store_location':info[3],'cId':info[4]};
    
    def getEditCampaignInfo(campaignId,userId,isWeb=False):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        #get campaign info
        try:
                
            campaign = Multiple_campaign_upload.objects.get(id=campaignId,campaign_uploaded_by=userId)
            campaignInfo = CampaignInfo.objects.get(campaign_id=campaign);
            info = campaignInfo.info;
            infoObject = json.loads(info,encoding='utf-8');

            return {'statusCode':0,'duration':infoObject['duration'],
                'hide_ticker_txt':infoObject['hide_ticker_txt'],'campaign_name':campaign.campaign_name};
        except Multiple_campaign_upload.DoesNotExist:
                #check whether campaign is assigned or not
            return {'status':'inside error'};
            try:
                    campaign = Approved_Group_Campaigns.objects.get(user_id=userId,campaign_id=campaignId);
                    return {'statusCode':2,'status':'Dear  User,  This is Campaign is Shared from Group. you can not edit this campaign'}
            except:
                    return {'statusCode':2,'status':'Invalid campaign'}

    def editCampaign(campaignId,userId,postParams,isWeb=False):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        #get campaign info
        with transaction.atomic():
            try:
                campaign = Multiple_campaign_upload.objects.get(id=campaignId,campaign_uploaded_by=userId)
                campaignInfo = CampaignInfo.objects.get(campaign_id=campaign);
                info = campaignInfo.info;
                infoObject = json.loads(info,encoding='utf-8');
                if('duration' in postParams):
                    infoObject['duration'] = postParams.get('duration');
                if('hide_ticker_txt' in postParams):
                    if(postParams.get('hide_ticker_txt') == "true"):
                        infoObject['hide_ticker_txt'] = True;
                    else:
                        infoObject['hide_ticker_txt'] = False
                    
                
                campaignInfo.info = json.dumps(infoObject,ensure_ascii=False);
                campaignInfo.save();

                campaign.updated_date = timezone.now()
                campaign.save();
                return {'statusCode':0,'status':'Campaign has been edited successfully'};
            except Multiple_campaign_upload.DoesNotExist:
                #check whether campaign is assigned or not
                try:
                    campaign = Approved_Group_Campaigns.objects.get(user_id=userId,campaign_id=campaignId);
                    return {'statusCode':2,'status':'Dear  User,  This is Campaign is Shared from Group. you can not edit this campaign'}
                except:
                    return {'statusCode':2,'status':'Invalid campaign'}

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
    schedule_type = models.SmallIntegerField(default=10)#10->schedule always
    pc_priority = models.IntegerField(default=0)
    is_skip = models.SmallIntegerField(default=0)#0->false, 1->skip true
    
    class Meta(object):
        unique_together = [
        ['user','player','campaign']
        ]
    
    def getPlayerCampaign(player,campaign,userId):
        try:
            playerCampaign = Player_Campaign.objects.get(user_id=userId,player_id=player,campaign_id=campaign);
            return playerCampaign;
        except Player_Campaign.DoesNotExist:
            return False;

    def getCampaignsInfo(userId,playerId,isUserId=False):
        if(isUserId == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        #get group info
        try:
            #playerInfo = Player.objects.get(id=playerId,user_id=userId);
            with connection.cursor() as cursor:
                conditionQuery = '''SELECT campaigns.*, camInfo.info,pc_campaign.is_skip as is_skip FROM campaign_player_campaign as pc_campaign 
                    INNER JOIN cmsapp_multiple_campaign_upload as campaigns  ON pc_campaign.campaign_id = campaigns.id 
                    LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE ( 
                         pc_campaign.user_id=%s and pc_campaign.player_id= %s) 
                    group by campaigns.id ORDER BY campaigns.updated_date DESC'''
                
                cursor.execute(conditionQuery,[userId,playerId])
                campaigns = dictfetchall(cursor);
                cursor.close();
                connection.close();
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
                playerInfo = Player.canAccessPlayer(pId,userId);
                
                #check for campaigns (provided campaigns must be user uploaded)
                if(Player_Campaign.checkForvalidCampaigns(campaigns,userId)):
                    
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
    
    def checkForvalidCampaigns(campaigns,userId):
        parameters = campaigns.copy();
        
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT count(*)  FROM cmsapp_multiple_campaign_upload as campaigns WHERE id IN ({}) 
            AND (campaigns.campaign_uploaded_by =  %s OR campaigns.id IN ( 
                    SELECT campaign_id FROM campaign_approved_group_campaigns WHERE user_id=%s )) 
                '''.format(','.join(['%s' for _ in range(len(campaigns))]))
            
            parameters.append(userId);
            parameters.append(userId);
            cursor.execute(conditionQuery,parameters)
            checkedCampaigns = cursor.fetchone();
            if(checkedCampaigns == None):
                return False;
            else:
                return (checkedCampaigns[0] == (len(campaigns)))

    def assignCampaignsToPlayers(userId,players,campaignId,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           players =  json.loads(players);
           
           return Player_Campaign.addCampaignsToPlayer(userId,players,campaignId);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Player has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};

    def addCampaignsToPlayer(userId,players,campaignId):
        if(campaignId and int(campaignId)>=1 and players and len(players)>=1):
            #check group info
            try:
                #check for player,,
                playerInfo = Player.objects.filter(id__in=players,user_id=userId);
                if(len(playerInfo)!=len(players)):
                    return {'statusCode':5,'status':
                    'Some of the players are not found, please refresh and try again later'};

                #check for campaigns (provided campaigns must be user uploaded)
                campaigns = [];
                campaigns.append(campaignId);
                if(Player_Campaign.checkForvalidCampaigns(campaigns,userId)):
                    
                    #prepare object to bulk insert
                    campaignsBulk = [];
                    for playerId in players:
                        campaignsBulk.append(
                            Player_Campaign(user_id=userId,player_id=playerId,campaign_id=campaignId));

                    Player_Campaign.objects.bulk_create(campaignsBulk);
                    
                    return {'statusCode':0,'status':
                    'Campaigns have been published successfully'};
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
                
            except Player_Campaign.DoesNotExist:
                return {'statusCode':4,
                'status':"Player not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};
    
    def skipCampaigns(userId,pId,cId,isSkip,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        try:
           playerCampaign = Player_Campaign.objects.get(user_id=userId,player_id=pId,campaign_id=cId); 
           playerCampaign.is_skip = isSkip;
           playerCampaign.save();
           return {'statusCode':0,'status':'Campaign has been skipped successfully'}
        except Player_Campaign.DoesNotExist:
            return {'statusCode':4,'status':'Campaign info not found, please try again later'};

    def getPlayerCampaignsWithInfo(player,secretKey):
        userId = User_unique_id.getUserId(secretKey);
        if(userId == False):
            return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT campaigns.*, camInfo.info,pc_campaign.is_skip as is_skip FROM campaign_player_campaign as pc_campaign 
                    INNER JOIN cmsapp_multiple_campaign_upload as campaigns  ON pc_campaign.campaign_id = campaigns.id 
                    LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE ( 
                         pc_campaign.user_id=%s and pc_campaign.player_id= %s) 
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

    def getPlayerScheduleCampaignsWithInfo(player,secretKey):
        userId = User_unique_id.getUserId(secretKey);
        if(userId == False):
            return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT campaigns.*, camInfo.info,schedules.id as sc_id, schedules.schedule_from, schedules.schedule_to, pc.schedule_type,schedules.schedule_type as sc_schedule_type, pc.pc_priority, schedules.sc_priority,schedules.additional_info,pc.is_skip as is_skip FROM  campaign_player_campaign as pc
                INNER JOIN cmsapp_multiple_campaign_upload as campaigns ON pc.campaign_id = campaigns.id
                LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id 
                LEFT JOIN campaign_schedule_campaign as schedules ON pc.id = schedules.player_campaign_id WHERE (pc.user_id=%s and pc.player_id= %s)
                ORDER BY campaigns.updated_date DESC'''
            
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

    def getDSPCampaigns(player,secretKey):
        userId = User_unique_id.getUserId(secretKey);
        if(userId == False):
            return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        with connection.cursor() as cursor:
            conditionQuery = '''SELECT campaigns.*, cinfo.info,sc.id as sc_id, sc.schedule_from, sc.schedule_to, pc.schedule_type,sc.schedule_type as sc_schedule_type, pc.pc_priority, sc.sc_priority,sc.additional_info,pc.is_skip as is_skip,pc.id as pc_id,dgc.id as dgc_id,dgc.dgc_schedule_type,dgc.dgc_priority,dgc.dgc_is_skip from cmsapp_multiple_campaign_upload as campaigns 
            INNER JOIN campaign_campaigninfo as cinfo on cinfo.campaign_id_id = campaigns.id
            LEFT JOIN campaign_player_campaign as pc on pc.campaign_id = campaigns.id AND pc.player_id = %s
            LEFT JOIN device_group_device_group_campaign as dgc on dgc.campaign_id = campaigns.id 
            LEFT JOIN campaign_schedule_campaign sc on pc.id = sc.player_campaign_id or dgc.id = sc.device_group_campaign_id
            WHERE ( (pc.user_id = %s or pc.player_id IN (SELECT player_id FROM group_player where player_id=%s AND gc_group_id IN (SELECT gc_group_id FROM group_gcgroupmembers WHERE status=1))) or dgc.device_group_id IN (SELECT device_group_id FROM device_group_device_group_player WHERE player_id=%s and device_group_id IN (SELECT id FROM device_group_device_group WHERE user_id = %s)))
            ORDER BY campaigns.updated_date DESC'''
            
            cursor.execute(conditionQuery,[player,userId,player,player,userId])
            campaigns = dictfetchall(cursor);
            cursor.close();
            connection.close();
        
        #campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
        if(len(campaigns)<=0):
            return {'statusCode':2,'status':
            'No campaigns Found'};
        else:
            return {'statusCode':0,'campaigns':campaigns};

from device_group.models import Device_Group_Campaign
class Schedule_Campaign(models.Model):
    
    player_campaign = models.ForeignKey('campaign.Player_Campaign',on_delete=models.CASCADE,null=True)
    device_group_campaign = models.ForeignKey('device_group.Device_Group_Campaign',on_delete=models.CASCADE,null=True)
    schedule_from = models.DateTimeField(null=False,blank=False)
    schedule_to = models.DateTimeField(null=False,blank=False)
    schedule_type = models.SmallIntegerField(default=10)#10->schedule always
    sc_priority = models.IntegerField(default=0)
    additional_info = models.TextField(null=True)
    

    class Meta:
       indexes = [
           models.Index(fields=['schedule_from', 'schedule_to',]),
           ]
    
    
    def saveCampaign(isWeb,accessToken,scheduleFrom,scheduleTo,pcId,scheduleType,
        scPriority,additionalInfo):
        if(isWeb==False):
            accessToken = User_unique_id.getUserId(accessToken);
            if(accessToken == False):
                return {'statusCode':2,'status':
                "Invalid session, please login"};
        try:
            pcInfo = Player_Campaign.objects.get(id=pcId,user_id=accessToken);
            scheduleFrom = datetime.datetime.strptime(scheduleFrom,"%Y-%m-%d %H:%M:%S")
            scheduleFrom = scheduleFrom.astimezone(pytz.UTC);
            scheduleTo = datetime.datetime.strptime(scheduleTo,"%Y-%m-%d %H:%M:%S")
            scheduleTo = scheduleTo.astimezone(pytz.UTC);
            if(scheduleFrom >= scheduleTo):
                return {'statusCode':7,'status':'Invalid times','scheduleFrom':scheduleFrom.now(),'scheduleTo':scheduleTo.now()};
            
            isTimeSlotAvailable = True;
            
            with connection.cursor() as cursor:
                mhnSchedule = ['100','110','120'];
                checkSlotQuery=None;cursorParams=[];
                if scheduleType in mhnSchedule:
                    checkSlotQuery = ''' SELECT count(*) FROM campaign_schedule_campaign WHERE
                    player_campaign_id = %s AND ((schedule_from <= %s AND schedule_to >= %s) OR (schedule_from <= %s AND schedule_to >= %s) OR (schedule_from >= %s AND schedule_to <= %s)) AND 
                    schedule_type IN ({})'''.format(','.join(['%s' for _ in range(len(mhnSchedule))]))
                    cursorParams = [pcId,scheduleTo,scheduleTo,scheduleFrom,scheduleFrom,scheduleFrom,scheduleTo];
                    for i in mhnSchedule:
                        cursorParams.append(i);
                
                elif(scheduleType=='200' or scheduleType == '250' or scheduleType == '300'):
                    checkSlotQuery = ''' SELECT count(*) FROM campaign_schedule_campaign WHERE 
                    player_campaign_id = %s  AND schedule_type = %s AND schedule_from = datetime(%s)'''
                    cursorParams = [pcId,scheduleType,scheduleFrom];
                
                if(checkSlotQuery is not None):
                    cursor.execute(checkSlotQuery,cursorParams);  
                    info = cursor.fetchone();
                
                    if (info[0] >=1):
                        isTimeSlotAvailable = False;

            if(isTimeSlotAvailable==False):
                return {'statusCode':5,'status':'Campaign has been scheduled for the selected times, please select different time'};
            else:
                #return {'status':True,'info':info}
                with transaction.atomic():
                    #update schedule type
                    pcInfo.schedule_type=100;#schedule
                    pcInfo.save();
                    #save the values
                    newScheduleCampaign = Schedule_Campaign();
                    newScheduleCampaign.player_campaign_id = pcId;
                    newScheduleCampaign.schedule_from = scheduleFrom
                    newScheduleCampaign.schedule_to = scheduleTo
                    newScheduleCampaign.schedule_type= scheduleType
                    newScheduleCampaign.sc_priority = scPriority
                    newScheduleCampaign.additional_info = additionalInfo
                    newScheduleCampaign.save();
                    
                    if(newScheduleCampaign.id>=1):
                        return {'statusCode':0,'status':'Schedule has been saved successfull','id':newScheduleCampaign.id,
                        'sc_priority':newScheduleCampaign.sc_priority,'additional_info':newScheduleCampaign.additional_info};
                    else:
                        return {'statusCode':6,'status':'Some thing went wrong, please try again later'};
        except Player_Campaign.DoesNotExist:
            return {'statusCode':4,'status':'Invalid info, campaign not found'}
        except Exception as e:    
            return {'statusCode':6,'status':e.args}

    def saveDGCSchedule(isWeb,accessToken,scheduleFrom,scheduleTo,scheduleType,
        scPriority,additionalInfo,dgcId):
        if(isWeb==False):
            accessToken = User_unique_id.getUserId(accessToken);
            if(accessToken == False):
                return {'statusCode':2,'status':
                "Invalid session, please login"};
        try:
            dgcInfo = Device_Group_Campaign.objects.get(id=dgcId,device_group__user_id=accessToken);
            scheduleFrom = datetime.datetime.strptime(scheduleFrom,"%Y-%m-%d %H:%M:%S")
            scheduleFrom = scheduleFrom.astimezone(pytz.UTC);
            scheduleTo = datetime.datetime.strptime(scheduleTo,"%Y-%m-%d %H:%M:%S")
            scheduleTo = scheduleTo.astimezone(pytz.UTC);
            if(scheduleFrom >= scheduleTo):
                return {'statusCode':7,'status':'Invalid times','scheduleFrom':scheduleFrom.now(),'scheduleTo':scheduleTo.now()};
            
            isTimeSlotAvailable = True;
            
            with connection.cursor() as cursor:
                mhnSchedule = ['100','110','120'];
                checkSlotQuery=None;cursorParams=[];
                if scheduleType in mhnSchedule:
                    checkSlotQuery = ''' SELECT count(*) FROM campaign_schedule_campaign WHERE
                    device_group_campaign_id = %s AND ((schedule_from <= %s AND schedule_to >= %s) OR (schedule_from <= %s AND schedule_to >= %s) OR (schedule_from >= %s AND schedule_to <= %s)) AND 
                    schedule_type IN ({})'''.format(','.join(['%s' for _ in range(len(mhnSchedule))]))
                    cursorParams = [dgcId,scheduleTo,scheduleTo,scheduleFrom,scheduleFrom,scheduleFrom,scheduleTo];
                    for i in mhnSchedule:
                        cursorParams.append(i);
                
                elif(scheduleType=='200' or scheduleType == '250' or scheduleType == '300'):
                    checkSlotQuery = ''' SELECT count(*) FROM campaign_schedule_campaign WHERE 
                    device_group_campaign_id = %s  AND schedule_type = %s AND schedule_from = datetime(%s)'''
                    cursorParams = [dgcId,scheduleType,scheduleFrom];
                
                if(checkSlotQuery is not None):
                    cursor.execute(checkSlotQuery,cursorParams);  
                    info = cursor.fetchone();
                
                    if (info[0] >=1):
                        isTimeSlotAvailable = False;

            if(isTimeSlotAvailable==False):
                return {'statusCode':5,'status':'Campaign has been scheduled for the selected times, please select different time'};
            else:
                #return {'status':True,'info':info}
                with transaction.atomic():
                    #update schedule type
                    dgcInfo.dgc_schedule_type=100;#schedule
                    dgcInfo.save();
                    #save the values
                    newScheduleCampaign = Schedule_Campaign();
                    newScheduleCampaign.device_group_campaign_id = dgcId;
                    newScheduleCampaign.schedule_from = scheduleFrom
                    newScheduleCampaign.schedule_to = scheduleTo
                    newScheduleCampaign.schedule_type= scheduleType
                    newScheduleCampaign.sc_priority = scPriority
                    newScheduleCampaign.additional_info = additionalInfo
                    newScheduleCampaign.save();
                    
                    if(newScheduleCampaign.id>=1):
                        return {'statusCode':0,'status':'Schedule has been saved successfull','id':newScheduleCampaign.id,
                        'sc_priority':newScheduleCampaign.sc_priority,'additional_info':newScheduleCampaign.additional_info};
                    else:
                        return {'statusCode':6,'status':'Some thing went wrong, please try again later'};
        except Device_Group_Campaign.DoesNotExist:
            return {'statusCode':4,'status':'Invalid info, campaign not found'}
        except Exception as e:    
            return {'statusCode':6,'status':e.args}


    def getPCSchedules(pcId):
        schedules = Schedule_Campaign.objects.filter(player_campaign_id=pcId).order_by('-id');
        return list(schedules.values());

    def getDGCSchedules(dgcId):
        schedules = Schedule_Campaign.objects.filter(device_group_campaign_id=dgcId).order_by('-id');
        return list(schedules.values());

    def deleteCampaignSchedule(isWeb,accessToken,scId,scType="pc"):
        if(isWeb==False):
            accessToken = User_unique_id.getUserId(accessToken);
            if(accessToken == False):
                return {'statusCode':2,'status':
                "Invalid session, please login"};
        #return {'datetime':timezone.now()}
        try:
            if(scType=="dg"):
                scheduleCampaign = Schedule_Campaign.objects.get(id=scId,device_group_campaign__device_group__user_id=accessToken);
            else:
                scheduleCampaign = Schedule_Campaign.objects.get(id=scId,player_campaign__user_id=accessToken);  
            if((scheduleCampaign.schedule_to)>timezone.now()):
                dgcId = scheduleCampaign.device_group_campaign_id;
                pcId = scheduleCampaign.player_campaign_id;
                scheduleCampaign.delete();
                #check and update schedule type
                if(scType=="dg"):
                    #get all schedules 
                    count = Schedule_Campaign.objects.filter(device_group_campaign_id=dgcId).values('device_group_campaign_id');
                    if(len(count)<=0):
                        #update campaign type in device_group_campaign
                        dgcInfo = Device_Group_Campaign.objects.get(id=dgcId);
                        dgcInfo.dgc_schedule_type = 10;
                        dgcInfo.save();
                else:
                    count = Schedule_Campaign.objects.filter(player_campaign_id=pcId).values('player_campaign_id');
                    if(len(count)<=0):
                        #update campaign type in device_group_campaign
                        pcInfo = Player_Campaign.objects.get(id=pcId);
                        pcInfo.schedule_type = 10;
                        pcInfo.save();
 
                return {'statusCode':0,'status':'Schedule has been removed successfully'};
            else:
                return {'statusCode':7,'status':'Cannot delete an expired schedule'};
        except Schedule_Campaign.DoesNotExist:
            return {'statusCode':6,'status':'Unable to delete schedule, please try again later type'+scType+",scId"+scId};