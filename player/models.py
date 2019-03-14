from django.db import models
from django.conf import settings
import datetime
from datetime import datetime as dt
import json


# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    mac = models.CharField(max_length=20,blank=False,null=False)
    name = models.CharField(max_length=25,blank=False,null=False)
    status = models.SmallIntegerField(default=0)#0->in trail, 1->activated, -1->expired
    fcm_id = models.CharField(max_length=125)
    expiry_date = models.DateTimeField()
    registered_at = models.DateTimeField(default=datetime.datetime.now())
    activated_by = models.CharField(max_length=25,default=0)#0 is self

    class Meta(object):
        unique_together=[
        ['mac']
        ]

    def __str__(self):
        return self.mac

    def registerPlayer(data,userId):
        try:
           data =  json.loads(data);
           try:
            player = Player.objects.get(mac=data['mac'])
            
           except Player.DoesNotExist:
            player = Player(user_id=userId,mac=data['mac']);
            player.expiry_date = dt.now() + datetime.timedelta(days=15);
           player.name = data["name"];
           player.fcm_id = data['fcm_id'];
           player.save();
           return {'statusCode':0,'status':player.status,'player':player.id,'mac':data['mac'],
           'fcm':player.fcm_id};
        except Exception as ex:
           return {'statusCode':5,'status':'unable to register - '+str(ex)};
         
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters,  - "+str(ex)}

    def refreshFCM(playerId,playerMac,fcm):
      try:
        player = Player.objects.get(id=playerId,
          mac=playerMac);
        player.fcm_id = fcm;
        player.save();
        return True;
      except Player.DoesNotExist:
        return False;

    def getPlayer(playerId,playerMac):
      try:
        player = Player.objects.get(id=playerId,
          mac=playerMac);
        return player.id;
      except Player.DoesNotExist:
        return False;

    def getMyPlayers(userId):
      player = Player.objects.filter(user_id=userId);
      return list(player.values());

    def isMyPlayer(playerId,userId):
      try:
        player = Player.objects.get(id=playerId,
          user_id=userId);
        return player;
      except Player.DoesNotExist:
        return False;


#metrics modal
class Metrics(models.Model):
  player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
  file_path=models.FileField(upload_to="player_metrics/")

  def saveRec(player,file_path):
    try:
      record = Metrics(player_id=player,file_path=file_path)
      record.save();
      return True
    except Exception as e:
      return False;

class Age_Geder_Metrics(models.Model):
  player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=datetime.datetime.now(),blank=False,null=False)
  g_male=models.IntegerField(default=0)
  g_female=models.IntegerField(default=0)
  age_0_2 = models.IntegerField(default=0)
  age_4_6 = models.IntegerField(default=0)
  age_8_12 = models.IntegerField(default=0)
  age_15_20 = models.IntegerField(default=0)
  age_25_32 = models.IntegerField(default=0)
  age_38_43 = models.IntegerField(default=0)
  age_48_53 = models.IntegerField(default=0)
  age_60_100 = models.IntegerField(default=0)
  
  def saveMetrics(player,genders,ages):
    try:
      metrics = Age_Geder_Metrics(player_id=player);
      #save gender metrics
      if "Female" in genders:
        metrics.g_female = genders['Female'];
      if "Male" in genders:
        metrics.g_male = genders['Male']

      #age metrics 
      for age in ages:
        if age == "0":
          metrics.age_0_2 = ages[age];
        elif age == "1":
          metrics.age_4_6 = ages[age];
        elif age == "2":
          metrics.age_8_12 = ages[age];
        elif age == "3":
          metrics.age_15_20 = ages[age];
        elif age == "4":
          metrics.age_25_32 = ages[age];
        elif age == "5":
          metrics.age_38_43 = ages[age];
        elif age == "6":
          metrics.age_48_53 = ages[age];
        elif age == "7":
          metrics.age_60_100 = ages[age];

      metrics.save();
      if(metrics.id>=1):
        return {'statusCode':0}
      else:
        return {'statusCode':1,'status':"Unable to save metrics"};
    except Exception as ex:
      return {'statusCode':1,'status':"Unable to save metrics - "+str(ex)};

  def getViewerMetrics(secretKey,isUserId,postParams):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
      # check for player
      if(Player.isMyPlayer(postParams.get('player'),secretKey)):
        return True