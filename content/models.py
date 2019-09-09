from django.db import models
import uuid 
import time
from django.db import transaction
import json
from cmsapp.models import User_unique_id
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Q
from django.db.models import Count

class Content(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=125,null=False,blank=False)
    access_level = models.SmallIntegerField(default=0)#0->private,1->public
    store_location = models.SmallIntegerField(default=2)#1->local,2->db
    file_path = models.TextField(default="")
    file_name = models.CharField(max_length=125,default="")

    def initUpload(postData,accessToken,storeLocation,
        isWeb,userEmailId):
        userId = accessToken;
        if(isWeb==False):
            userId = User_unique_id.getUserId(accessToken);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
            userEmailId = User.objects.get(id=userId).email;
        #uniqueKey = str(uuid.uuid4().hex[:6].upper())+str(round(time.time() * 1000))+uuid.uuid4().hex[:6];
        savePath = '/content/{}/'.format(userEmailId);
        return Content.saveContent(userId,postData,savePath);

    def saveContent(userId,postData,savePath):
        try:
            with transaction.atomic():
                #save content to table
                content = Content(
                    user_id=userId,
                    description=postData.get('description'),
                    access_level=postData.get('access_level'),
                    file_path=savePath,
                    file_name=postData.get('file_name'));
                if('store_location' in postData):
                    content.store_location = postData.get('store_location');
                content.save();
                if('keys' in postData):
                    contentKeys = json.loads(postData.get('keys'));
                    keysData = [];
                    for contentKey in contentKeys:
                        keysData.append(Content_Key(content_id=content.id,
                            key=contentKey));
                    Content_Key.objects.bulk_create(keysData);

                return {'statusCode':0,'status':'content saved successfully',
                'content_id':content.id,'save_path':savePath};
        except Exception as e:
            return {'statusCode':6,
                'status':'Unable to save details '+str(e)};

    def canUploadContentResource(accessToken,contentId,isWeb):
        userId=accessToken;
        if(isWeb==False):
            userId = User_unique_id.getUserId(accessToken);
            if(userId == False):
                return {'statusCode':1,'status':
                         "Invalid session, please login"};

        try:
            content = Content.objects.get(id=contentId,user_id=userId);
            return {'statusCode':0,'content':content};
        except Multiple_campaign_upload.DoesNotExist:
           return {'statusCode':1,'status':'No content found'}; 
    
    def getTotalContent(userId):
       
        contents = Content.objects.values('user_id').annotate(t_count=Count('user_id')).filter(user_id=userId)
        if(len(contents)>=1):
            return (contents[0]['t_count']);
        return 0;

class Content_Key(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    key= models.CharField(max_length=125,null=False,blank=False)

