from django.db import models
from cmsapp.models import Multiple_campaign_upload
import json
from cmsapp.models import User_unique_id
import datetime
from django.db import transaction

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
            savePath = '{}/{}/'.format(secretKey,campaignName);
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