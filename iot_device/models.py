from django.db import models
from django.conf import settings

# Create your models here.

class IOT_Device(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	mac = models.CharField(max_length=125,blank=False,null=False,unique=True,db_index=True)
	name = models.CharField(max_length=50,blank=False,null=False)
	device_type = models.CharField(max_length=50,blank=False,null=False)

