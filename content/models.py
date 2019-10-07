from django.db import models

from django.db import transaction
import json
from cmsapp.models import User_unique_id
from django.contrib.auth.models import User

# Create your models here.

from django.db.models import Count
import datetime
from django.core import serializers

from signagecms import constants
import os
from django.http import JsonResponse
import requests


class Content(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=125,null=False,blank=False)
    access_level = models.SmallIntegerField(default=0)#0->private,1->public
    store_location = models.SmallIntegerField(default=2)#1->local,2->db
    file_path = models.TextField(default="")
    file_name = models.CharField(max_length=125,default="")
    content_type = models.CharField(max_length=15,default="image")
    created_at = models.DateTimeField(default=datetime.datetime.now())
    is_approved = models.SmallIntegerField(default=0)#0->false, 1-> true

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
                    file_name=postData.get('file_name'),
                    content_type=postData.get('content_type'));
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
    
    def getTotalContent(userId,cType="all"):
       
        contents = Content.objects.values('user_id').annotate(t_count=Count('user_id')).filter(user_id=userId)
        if (cType != "all"):
            contents = contents.filter(content_type=cType);
        if(len(contents)>=1):
            return (contents[0]['t_count']);
        return 0;

    def getMyContent(userId,limit,offset,cType="all"):
        myContent = Content.objects.filter(user_id=userId);
        if(cType!="all"):
            myContent = myContent.filter(content_type=cType);
        
        myContent = myContent.order_by('-id')[offset:(offset+limit)]    
        
        if(myContent.exists()):
            return {'statusCode':0,'content':list(myContent.values())};
        else:
            return {'statusCode':2,'status':'No content found'};

    def getContentInfo(cId,userId):
        try:
            content = Content.objects.get(id=cId,user_id=userId);
            content = serializers.serialize('json', [ content, ]);
            content = json.loads(content);
            return {'statusCode':0,
            'content':content[0].get('fields')};
        except Content.DoesNotExist:
            return {'statusCode':2,'status':'content not found'};
    
    
    def deleteMyContent(contentId,accessToken,isWeb):
        userId=accessToken;
        if(isWeb==False):
            userId = User_unique_id.getUserId(accessToken);
            if(userId == False):
                return {'statusCode':1,'status':
                         "Invalid session, please login"};
        try:
            content = Content.objects.get(id=contentId,user_id=userId);
            savePath = content.file_path+str(content.file_name);

            #return {'savePath':savePath}
            storeLocation = content.store_location;
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
                    os.remove(campaignPath)
                    #shutil.rmtree(campaignPath);
            content.delete();
            return {'statusCode':0,'status':'Campaign has been deleted successfully'};
            
        except Content.DoesNotExist as e:
            return {'statusCode':3,'status':'Error -'+str(e)};

class Content_Key(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    key= models.CharField(max_length=125,null=False,blank=False)

