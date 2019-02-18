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

def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your models here.
class CampaignInfo(models.Model):
    campaign_id = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE,unique=True)
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
        
        isSave = self.createCampaign(userId,campaignName,campType,
            info,campaignSize);
        
        if(isSave == True):
            savePath = '/campaigns/{}/{}/'.format(secretKey,campaignName);
            return {'isSave':isSave,'statusCode':0,'status':
            "success",'save_path':savePath}
        else:
            return {'statusCode':3,'status':
            "Unable to upload campaign "+''.join(isSave)}
        

    @classmethod
    def createCampaign(cls,userId,name,campType,info,campaignSize):
        try:
         with transaction.atomic():
            #check for duplicate
            try:
                campaignToSave = Multiple_campaign_upload.objects.get(campaign_uploaded_by=userId,campaign_name=name)
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
            campaignToSave.save()
            
            #save info file
            try:
                campInfo = CampaignInfo.objects.get(campaign_id_id=campaignToSave.id)
            except CampaignInfo.DoesNotExist:
                campInfo = CampaignInfo()
                campInfo.campaign_id_id = campaignToSave.id
            campInfo.info = info
            campInfo.save()
         return True
        except Exception as e:
            
            return e.args
    
    #get campaigns created by user
    def getUserCampaigns(userId,isUserId=False):
        if(isUserId==False):
            userId = User_unique_id.getUserId(user_sessionId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
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
                LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE (campaigns.campaign_uploaded_by =  %s) 
                ORDER BY campaigns.updated_date DESC'''
            cursor.execute(conditionQuery,[userId])
            campaigns = dictfetchall(cursor);
            cursor.close();
        
        #campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
        if(len(campaigns)<=0):
            return {'statusCode':2,'status':
            'No campaigns Found'};
        else:
            return {'statusCode':0,'campaigns':campaigns};

    def deleteMyCampaign(campaignId,accessToken):
        userId = User_unique_id.getUserId(accessToken);
        if(userId == False):
            return {'statusCode':1,'status':
                "Invalid session, please login"};

        post_data = JsonResponse({ "path": "/campaigns/471f5bd2bcd24c5ab63e64ccd107e380/best tik tok" })
        headers = {'Authorization': 'Bearer {}'.format(constants.DROP_BOX_ACCESS_TOKEN),
        'Content-Type': 'application/json'}
        response = requests.post('https://api.dropboxapi.com/2/files/delete_v2', data=post_data,
            headers=headers);
        #print(response);
        content = response.content        
        return {'response':response.text};

    def listCampaigns1():
    
      with connection.cursor() as cursor:
        
        conditionQuery = '''SELECT campaigns.*,user.username as memberName,uniqueId.user_unique_key  FROM cmsapp_multiple_campaign_upload as campaigns 
                 INNER JOIN auth_user as user on campaigns.campaign_uploaded_by=user.id INNER JOIN cmsapp_user_unique_id as uniqueId on user.id = uniqueId.user_id 
                 WHERE stor_location = 2  '''
        cursor.execute(conditionQuery)
        campaigns = dictfetchall(cursor);
        cursor.close();
        return {'campaigns':campaigns,'total':len(campaigns)}

    def updateSavePath(userId,accessToken):
        campaigns = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=userId);
        path="no";
        i=0;
        for campaign in campaigns:
            newPath = "/campaigns/{}/{}/".format(accessToken,campaign.campaign_name)
            campaign.save_path = newPath;
            campaign.save();
            ++i;
           

        return {'path':newPath,'userId':userId,'total':len(campaigns),
        'updated':i};