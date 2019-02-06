from django.db import models
from cmsapp.models import Multiple_campaign_upload
import json
from cmsapp.models import User_unique_id
import datetime
from django.db import transaction, connection
from signagecms import constants
import requests 

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
                LEFT JOIN campaign_campaigninfo as camInfo ON campaigns.id = camInfo.campaign_id_id WHERE (campaigns.campaign_uploaded_by =  %s)'''
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

        post_data = {'name': 'Gladys'}
        headers = {'Authorization': 'Bearer {}'.format(constants.API_HOST),
        'Content-Type': 'application/json'}
        response = requests.post('https://api.dropboxapi.com/2/files/delete_v2', data=post_data,
            headers=headers);
        #print(response);
        content = response.content        
        return response;
