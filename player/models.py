from django.db import models
from django.conf import settings
import datetime
from datetime import datetime as dt
import json
from cmsapp.models import User_unique_id
from django.db import  connection

def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    mac = models.CharField(max_length=20,blank=False,null=False)
    name = models.CharField(max_length=25,blank=False,null=False)
    status = models.SmallIntegerField(default=0)#0->in trail, 1->activated, -1->expired
    fcm_id = models.CharField(max_length=250)
    expiry_date = models.DateTimeField()
    registered_at = models.DateTimeField(default=datetime.datetime.now())
    activated_by = models.CharField(max_length=25,default=0)#0 is self
    location_desc = models.CharField(max_length=25,default="")
    
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
            player = Player(mac=data['mac']);
            player.expiry_date = dt.now() + datetime.timedelta(days=15);
           
           player.user_id = userId;
           player.name = data["name"];
           if('fcm_id' in data):
            player.fcm_id = data['fcm_id'];
           
           if('location_desc' in data):
            player.location_desc = data['location_desc'];
            
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
    
    def getPlayers(secretKey,isUserId):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
      players = Player.getMyPlayers(userId);
      if(len(players)>=1):
        return {'statusCode':0,'players':players}
      else:
        return {'statusCode':2,'status':'No players found'};
        
    def isMyPlayer(playerId,userId,isPlayerId=True):
      try:
        player=None;
        if(isPlayerId==True):
          player = Player.objects.get(id=playerId,
            user_id=userId);
        else:
          player = Player.objects.get(mac=playerId,
            user_id=userId);
        return player;
      except Player.DoesNotExist:
        return False;



    def listPlayersToPublishCamp(campaignId,userId):
      
      with connection.cursor() as cursor:
          query = '''SELECT player.id,player.name,player_campaign.id as pcId FROM player_player as player 
           LEFT JOIN campaign_player_campaign as player_campaign ON player.id = player_campaign.player_id AND player_campaign.campaign_id=%s 
           WHERE (player.user_id=%s)'''
          cursor.execute(query,[campaignId,userId]);
          players = dictfetchall(cursor);
          cursor.close();
          connection.close();
        
      return {'statusCode':0,'players':players};
    
    def checkForvalidPlayers(players,userId):
      playerInfo = Player.objects.filter(id__in=players,user_id=userId);
      return (len(playerInfo)!=len(players));
    
    def canAccessPlayer(playerId,userId):
      query = '''SELECT player.name as player__name, player.id as player__id FROM player_player as player 
                 WHERE player.id = %s AND (player.user_id = %s or player.id IN (SELECT player_id FROM group_player where gc_group_id IN (SELECT gc_group_id FROM group_gcgroupmembers WHERE member_id =%s and status=1))) LIMIT 1'''
      params = (playerId,userId,userId);
      with connection.cursor() as cursor:
        cursor.execute(query,params);
        players = dictfetchall(cursor);
        if(len(players)>=1):
          return {'statusCode':0,'metrics':players[0]}
        else:
          return False;

    def getMyAssignedPlayers(userId):
      query = '''SELECT player.name as player__name, player.id as player__id, datetime(metrics.accessed_at,'localtime') as accessed_at FROM player_player as player 
                 LEFT JOIN player_last_seen_metrics as metrics on player.id= metrics.player_id 
                 WHERE player.user_id = %s or player.id IN (SELECT player_id FROM group_player where gc_group_id IN (SELECT gc_group_id FROM group_gcgroupmembers WHERE member_id =%s and status=1))
                 ORDER BY metrics.accessed_at DESC'''

      params = (userId,userId);
      with connection.cursor() as cursor:
        cursor.execute(query,params);
        players = dictfetchall(cursor);
        if(len(players)>=1):
          return {'statusCode':0,'metrics':players}
        else:
          return {'statusCode':1,'status':'No players'}

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
     
      metrics.created_at = datetime.datetime.now();
      metrics.save();
      if(metrics.id>=1):
        return {'statusCode':0}
      else:
        return {'statusCode':1,'status':"Unable to save metrics"};
    except Exception as ex:
      return {'statusCode':1,'status':"Unable to save metrics - "+str(ex)};

  def getViewerMetrics(secretKey,isUserId,postParams,exportExcel=False):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
      # check for player
      player = postParams.get('player');
      metrics={};
      if(player=="All"):
        #list all metrics
        metrics = Age_Geder_Metrics.objects.filter(player__user_id=userId,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).select_related('player').order_by('-created_at');
      
      elif(Player.isMyPlayer(player,userId)):
        metrics = Age_Geder_Metrics.objects.filter(player_id=player,
          created_at__range=[postParams.get('from_date'), postParams.get('to_date')]).order_by('-created_at');

      if(metrics.exists()):
          if(exportExcel==False):
            return {'statusCode':0,'metrics':list(metrics.values('created_at','g_female','g_male','player__name','age_0_2','age_4_6','age_8_12',
              'age_15_20','age_25_32','age_38_43','age_48_53','age_60_100'))}
          else:
            return {'statusCode':0,'metrics':(metrics.values_list('player__name','created_at','g_male','g_female','age_0_2','age_4_6','age_8_12',
              'age_15_20','age_25_32','age_38_43','age_48_53','age_60_100'))}
      else:
          return {'statusCode':4,'status':"No metrics found for the selected dates"};

class Last_Seen_Metrics(models.Model):
  player = models.OneToOneField('player.Player',on_delete=models.CASCADE,primary_key=True)
  accessed_at = models.DateTimeField(default=datetime.datetime.now(),blank=False,null=False)
  
  def __str__(self):
        return self.player.mac

  def saveMetrics(playerId):
    try:
      metrics = Last_Seen_Metrics.objects.get(player_id=playerId);
    except:
      metrics = Last_Seen_Metrics(player_id=playerId);

    metrics.accessed_at= datetime.datetime.now();
    metrics.save();

  def getMetrics(userId):
    metrics = Last_Seen_Metrics.objects.filter(player__user_id = userId).order_by('-accessed_at');
    if(metrics.exists()):
      return {'statusCode':0,'metrics':list(metrics.values('player__id','player__name','accessed_at'))}
    else:
      return {'statusCode':1,'status':'No metrics'}

from django.db.models import Sum, Max
class Campaign_Reports(models.Model):
    player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
    #campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',default=None,blank=True,null=True,on_delete=models.SET_NULL)
    campaign_id= models.IntegerField(default=0)
    campaign_name = models.CharField(max_length=50)
    times_played = models.SmallIntegerField(default=1)
    duration = models.IntegerField(default=1)
    last_played_at = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return self.player.mac
        
    def saveCampaignReports(player,pMac,data):
      try:
        data = json.loads(data);
        #check for player info,, if found save metrics
        Player.objects.get(id=player,mac=pMac);
        metrics=[];
        for report in data:
          p_metrics = Campaign_Reports(player_id=player,
            campaign_name=report['c_name'],times_played=report['times_played'],
            duration=report['duration'],last_played_at=report['last_played_at'],created_at=datetime.datetime.now());
          if('c_server_id' in report and report['c_server_id']>=1):
            p_metrics.campaign_id = report['c_server_id'];
          
          metrics.append(p_metrics);
  

        Campaign_Reports.objects.bulk_create(metrics);
        return {'statusCode':0,'status':'metrics'};

      except ValueError as ex:
        return {'statusCode':3,'status':
                "Invalid request parameters, data should not be zero - "+str(ex)};
      except Player.DoesNotExist:
        return {'statusCode':3,'status':
                "Player not found"};

    def getCampaignReports(secretKey,isUserId,postParams,exportReports=False):
      userId = secretKey;
      if(isUserId==False):
            userId = User_unique_id.getUserId(secretKey);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
      # check for player
      player = postParams.get('player');
      partners = [];
      #check for partner filters
      if 'partners' in postParams:
        try:
          partners = json.loads(postParams.get('partners'));
        except ValueError:
          partners = [];

      metrics={};
      params=[];
      if(player=="All"):
        params = [userId,postParams.get('from_date'),postParams.get('to_date')];
        #list all metrics
        if(len(partners)>=1):
          query = '''SELECT (user.first_name || " "||user.last_name) as campaign_owner,player.name as player__name, cr.campaign_name as campaign_name,sum(cr.times_played) as t_played, sum(cr.duration) as t_duration, max(last_played_at) as last_played_at, cr.campaign_id as campaign_id FROM player_player as player
          INNER JOIN player_campaign_reports as cr  ON player.id = cr.player_id
          LEFT JOIN cmsapp_multiple_campaign_upload as campaigns ON cr.campaign_id=campaigns.id
          LEFT JOIN auth_user as user ON campaigns.campaign_uploaded_by = user.id
          WHERE player.user_id = %s AND (cr.created_at BETWEEN %s AND %s) AND campaigns.campaign_uploaded_by IN ({}) GROUP BY cr.player_id,cr.campaign_name'''.format(','.join(['%s' for _ in range(len(partners))]))
          
          for partner in partners:
            params.append(partner);

        else:
          query = '''SELECT (user.first_name || " "||user.last_name) as campaign_owner,player.name as player__name, cr.campaign_name as campaign_name,sum(cr.times_played) as t_played, sum(cr.duration) as t_duration, max(last_played_at) as last_played_at, cr.campaign_id as campaign_id FROM player_player as player
          INNER JOIN player_campaign_reports as cr  ON player.id = cr.player_id
          LEFT JOIN cmsapp_multiple_campaign_upload as campaigns ON cr.campaign_id=campaigns.id
          LEFT JOIN auth_user as user ON campaigns.campaign_uploaded_by = user.id
          WHERE player.user_id = %s AND cr.created_at BETWEEN %s AND %s GROUP BY cr.player_id,cr.campaign_name'''
          
          
        
      else:
        params = [userId,player,postParams.get('from_date'),postParams.get('to_date')];
        if(len(partners)>=1):
          query = '''SELECT (user.first_name || " "||user.last_name) as campaign_owner,player.name as player__name, cr.campaign_name as campaign_name,sum(cr.times_played) as t_played, sum(cr.duration) as t_duration, max(last_played_at) as last_played_at, cr.campaign_id as campaign_id FROM player_player as player
          INNER JOIN player_campaign_reports as cr  ON player.id = cr.player_id
          LEFT JOIN cmsapp_multiple_campaign_upload as campaigns ON cr.campaign_id=campaigns.id
          LEFT JOIN auth_user as user ON campaigns.campaign_uploaded_by = user.id
          WHERE player.user_id = %s AND player.id = %s AND (cr.created_at BETWEEN %s AND %s) AND campaigns.campaign_uploaded_by IN ({}) GROUP BY cr.player_id,cr.campaign_name'''.format(
            (','.join(['%s' for _ in range(len(partners))])))
          
          for partner in partners:
            params.append(partner);
        else:
          query = '''SELECT (user.first_name || " "||user.last_name) as campaign_owner,player.name as player__name, cr.campaign_name as campaign_name,sum(cr.times_played) as t_played, sum(cr.duration) as t_duration, max(last_played_at) as last_played_at, cr.campaign_id as campaign_id FROM player_player as player
          INNER JOIN player_campaign_reports as cr  ON player.id = cr.player_id
          LEFT JOIN cmsapp_multiple_campaign_upload as campaigns ON cr.campaign_id=campaigns.id
          LEFT JOIN auth_user as user ON campaigns.campaign_uploaded_by = user.id
          WHERE player.user_id = %s AND player.id = %s AND (cr.created_at BETWEEN %s AND %s) GROUP BY cr.player_id,cr.campaign_name'''
          
      with connection.cursor() as cursor:
        cursor.execute(query,params);
        metrics = dictfetchall(cursor);
      
      if(len(metrics)>=1):
        if(exportReports==False):
          return {'statusCode':0,'metrics':metrics}
          #return {'statusCode':0,'metrics':list(metrics.values('campaign_name','t_played','t_duration','player__name','campaign_id','last_played_at')),'queryset.query':str(metrics.query),'params':params};
        else:
          return {'statusCode':0,'metrics':metrics}
          #return {'statusCode':0,'metrics':(metrics.values_list('player__name','campaign_name','t_played','t_duration','last_played_at')),'queryset.query':str(metrics.query)};
      else:
          return {'statusCode':4,'status':"No metrics found for the selected dates"};