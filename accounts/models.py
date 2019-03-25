# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User
import uuid
import time

# Create your models here.
class ForgotPwdSession(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    session_key = models.CharField(max_length=250,blank=False,null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
    	return self.user.email;

    def createSession(userId):   	
    	try:
    		session = ForgotPwdSession.objects.get(user_id=userId)
    		return session.session_key;
    	except ForgotPwdSession.DoesNotExist:
    		uniqueKey = str(uuid.uuid4().hex[:6].upper())+str(round(time.time() * 1000))+uuid.uuid4().hex[:6];
    		session = ForgotPwdSession(user_id=userId,session_key = uniqueKey);
    		session.save();
    		return uniqueKey;