# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Searched_videos(models.Model):
    keyword = models.CharField(max_length=20,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    videos_link =models.URLField(blank=True,null=True)
    created_date = models.DateTimeField()
    video_id = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):

        return self.video_id


class Searched_images(models.Model):
    keyword = models.CharField(max_length=20,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    images_link =models.URLField(blank=True,null=True)
    created_date = models.DateTimeField()
    image_id = models.CharField(max_length=20,blank=True,null=True)

class Searched_news(models.Model):
    keyword = models.CharField(max_length=20,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    image_link=models.URLField(blank=True,null=True)
    news_link =models.URLField(blank=True,null=True)
    created_date = models.DateTimeField()
    news_id = models.CharField(max_length=20,blank=True,null=True)


class Access_Token(models.Model):
    ss_username = models.CharField(max_length=20)
    ss_client_id = models.CharField(max_length=50)
    ss_client_secret = models.CharField(max_length=300)


class Youtube_links(models.Model):
    user = models.CharField(max_length=5,blank=True,null=True)
    keyword = models.CharField(max_length=20,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    video_link =models.URLField(blank=True,null=True)
    created_date = models.DateTimeField()
    vid_id = models.CharField(max_length=8,blank=True,null=True)

class Images_links(models.Model):
    user = models.CharField(max_length=5,blank=True,null=True)
    keyword = models.CharField(max_length=20,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    image_link =models.URLField(blank=True,null=True)
    created_date = models.DateTimeField()
    img_id = models.CharField(max_length=8,blank=True,null=True)

class News_links(models.Model):
    user = models.CharField(max_length=5,blank=True,null=True)
    keyword = models.CharField(max_length=20,blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    image =models.URLField(blank=True,null=True)
    news_link =models.URLField(blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    created_date = models.DateTimeField()
    new_id = models.CharField(max_length=8,blank=True,null=True)


class Testing(models.Model):
    test = models.ForeignKey(Searched_videos,on_delete=models.CASCADE)
    ky = models.CharField(max_length=20,blank=True,null=True)


class Upload(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    upload = models.FileField()
    #keys = models.CharField(max_length=200)
    desc= models.TextField()
    file_access_mode = models.CharField(max_length=8)
    file_type = models.CharField(max_length=8)
    group_id = models.CharField(max_length=200,blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)


class Keywords(models.Model):
    keys = models.CharField(max_length=20,blank=True,null=True)
    #uploaded = models.ForeignKey(Upload)
    upload_id = models.CharField(max_length=20,blank=True,null=True)


class My_GC_Groups(models.Model):
    group_created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)
    group_created_date = models.DateTimeField()


class Group_users_list(models.Model):
    group_id = models.CharField(max_length=10,blank=True,null=True)   #will remove later
    group_emails_list = models.TextField()
    saved_emails_date = models.DateTimeField()

class Rest(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    num = models.CharField(max_length=10)
class Campaign(models.Model):
    camp_uploaded_by = models.CharField(max_length=50)
    camp_folder = models.CharField(max_length=50)
    camp_name = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    upload = models.FileField(blank=True,null=True,upload_to="campaigns")
class Single_campaign_upload(models.Model):
    campaign_uploaded_by = models.CharField(max_length=10,blank = True ,null= True)
    campaign_name = models.CharField(max_length=50)
    text_file = models.FileField(blank=True,null=True,upload_to="campaigns/single_region")
    media_file = models.FileField(blank=True,null=True,upload_to="campaigns/single_region")
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()



class Multiple_campaign_upload(models.Model):
    campaign_uploaded_by = models.BigIntegerField()
    campaign_name = models.CharField(max_length=50)
    text_file = models.FileField(upload_to="campaigns/",blank=True,null=True)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    is_skip = models.SmallIntegerField(default=0)
    camp_type = models.SmallIntegerField(default=-1)
    stor_location = models.SmallIntegerField(default=1)
    campaign_size = models.CharField(max_length=50,default=0)

    class Meta(object):
        unique_together = [
        ['campaign_uploaded_by', 'campaign_name']
        ]

class Multiple_campaign_files(models.Model):
    Multiple_campaign = models.CharField(max_length=10)
    mul_files = models.FileField(upload_to="campaigns/",blank=True,null=True)

class User_unique_id(models.Model):
    user_id = models.CharField(max_length=10)
    user_unique_key = models.CharField(max_length=50)

    def getUserId(uniqueId):       
       try:
        userId = User_unique_id.objects.get(user_unique_key=uniqueId);
        return userId.user_id
       except User_unique_id.DoesNotExist:
        return False
    
    def getUniqueKey(userId):
       try:
        uniqueKey = User_unique_id.objects.get(user_id=userId);
        return uniqueKey.user_unique_key
       except User_unique_id.DoesNotExist:
        return False
#class Campaign_files(models.Model):
   # camp_files = models.FileField(blank=True,null=True,upload_to="campaigns")

'''class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user_details=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_images',blank=True,null=True)
    gender=models.CharField(max_length=5,choices=GENDER)

class Post(models.Model):
    posted_by=models.ForeignKey(User)
    post=models.TextField()
    posted_time=models.DateTimeField()

class Comments(models.Model):
    commented_by=models.ForeignKey(User)
    post_details=models.ForeignKey(Post)
    comment=models.TextField()
    upload_time=models.DateTimeField()
    upload_file=models.FileField(blank=True,null=True)'''


