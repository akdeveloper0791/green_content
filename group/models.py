from django.db import models
from django.conf import settings
from cmsapp.models import User_unique_id,Multiple_campaign_upload
import json
from django.contrib.auth.models import User
from django.db import transaction, connection
import datetime
from django.db import IntegrityError
from django.core import serializers

def dictfetchall(cursor):
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your models here.
class GcGroups(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=False,null=False)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    
    class Meta(object):
        unique_together = [
        ['user', 'name']
        ]

    def createGroup(accessToken,groupMembers,isWeb,name):
        if(isWeb != True):
            accessToken = User_unique_id.getUserId(accessToken);
            
            if(accessToken == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        try:
           members =  json.loads(groupMembers);
           return GcGroups.saveGroup(accessToken,name,members);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, members should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group already exist with same name, please use different name"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters, members should not be zero--"+str(e)};

        return {'statusCode':1,'status':
                "Invalid session, please login",'accessToken':accessToken};
    
    def saveGroup(userId,name,members):
        if(members and len(members)>=1 and name):
            userEmails = User.objects.filter(email__in=members);
            
            if(len(userEmails) < len(members)):
                #generate invalid users
                invalidUsers=[];
                if(len(userEmails)<=0):
                    invalidUsers = members;
                else:
                    userEmails = list(userEmails.values('id','email'));
                    validUsers=[];
                    for user in userEmails:
                        validUsers.append(user['email']);
                    for memberEmail in members:
                        if(memberEmail not in validUsers):
                            invalidUsers.append(memberEmail);
                return {'statusCode':4,'status':"Some of the entered members are not valid GC users, you can not add them to groups",
                'invalidUsers':invalidUsers};
            
            else:
                memberUsers = list(userEmails.values('id'));
                with transaction.atomic():
                    gcGroup = GcGroups();
                    gcGroup.user_id = userId
                    gcGroup.name = name
                    gcGroup.created_date = datetime.datetime.now()
                    gcGroup.updated_date = datetime.datetime.now()
                    gcGroup.save()
                    #campaignToSave.id
                    gcGroupMembers = [];
                    for memberUser in memberUsers:
                        gcGroupMember = GcGroupMembers(gc_group_id = gcGroup.id,
                            member_id = memberUser['id']);
                        gcGroupMembers.append(gcGroupMember);
                    #save group members
                    GcGroupMembers.objects.bulk_create(gcGroupMembers);
                return {'statusCode':0,"status":
                "Group has been created successfully"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};
    
    def listGroups(userId,isUserId=False):
        if(isUserId == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};

        groups = GcGroups.objects.filter(user=userId);
        if(len(groups)<=0):
            return {'statusCode':2,'status':
            'No campaigns Found'};
        else:
            return {'statusCode':0,'groups':list(groups.values())};

    def getGroupInfo(userId,groupId,isUserId=False):
        if(isUserId == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        #get group info
        try:
            grouInfo = GcGroups.objects.get(id=groupId,user_id=userId);

            with connection.cursor() as cursor:

                membersQuery = '''SELECT user.username as memberName, user.email as memberEmail, members.member_id as member_id,members.status FROM group_gcgroups as gcgroup 
                INNER JOIN group_gcgroupmembers as members on gcgroup.id = members.gc_group_id INNER JOIN 
                auth_user as user on members.member_id=user.id WHERE (gcgroup.id =  %s )'''
                cursor.execute(membersQuery,[groupId]);
                members = dictfetchall(cursor);
                
                campaignsQuery = '''SELECT campaigns.campaign_name,campaigns.id as campaign_id FROM group_gcgroups as gcgroup 
                INNER JOIN group_groupcampaigns as groupCampaign on gcgroup.id = groupCampaign.gc_group_id INNER JOIN 
                cmsapp_multiple_campaign_upload as campaigns on groupCampaign.campaign_id=campaigns.id WHERE (gcgroup.id =  %s )'''
                cursor.execute(campaignsQuery,[groupId]);
                campaigns = dictfetchall(cursor);

                cursor.close();
        
        
            return {'statusCode':0,'gInfo':serializers.serialize('json', [ grouInfo, ]),'members':members,
            'campaigns':campaigns};

        except GcGroups.DoesNotExist:
            return {'statusCode':2,'status':'Group not found'}
        

                

class GcGroupMembers(models.Model):
    gc_group = models.ForeignKey('group.GcGroups',on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)

    class Meta(object):
        unique_together= [
        ['gc_group','member']
        ]
    
    def assignNewMembers(userId,gId,members,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           members =  json.loads(members);
           return GcGroupMembers.addMember(userId,gId,members);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the members provided, please check and add again-"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};
    
    def addMember(userId,gId,members):
        if(members and len(members)>=1 and gId):
            userEmails = User.objects.filter(email__in=members);
            
            if(len(userEmails) < len(members)):
                #generate invalid users
                invalidUsers=[];
                if(len(userEmails)<=0):
                    invalidUsers = members;
                else:
                    userEmails = list(userEmails.values('id','email'));
                    validUsers=[];
                    for user in userEmails:
                        validUsers.append(user['email']);
                    for memberEmail in members:
                        if(memberEmail not in validUsers):
                            invalidUsers.append(memberEmail);
                return {'statusCode':4,'status':"Some of the entered members are not valid GC users, you can not add them to groups",
                'invalidUsers':invalidUsers};
            
            else:
                try:
                    groupInfo = GcGroups.objects.get(id=gId,user_id=userId);
                    memberUsers = list(userEmails.values('id'));
                
                    gcGroupMembers = [];
                    for memberUser in memberUsers:
                      gcGroupMember = GcGroupMembers(gc_group_id = gId,
                      member_id = memberUser['id']);
                      gcGroupMembers.append(gcGroupMember);
                    #save group members
                    GcGroupMembers.objects.bulk_create(gcGroupMembers);
                    return {'statusCode':0,"status":
                     "Members have been assigned successfully"};
                except GcGroups.DoesNotExist:
                    return {'statusCode':4,
                    'status':"Group not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};

    def removeMembers(userId,gId,members,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           members =  json.loads(members);
           return GcGroupMembers.checkAndRemoveMember(userId,gId,members);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the members provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};
    
    def checkAndRemoveMember(userId,gId,members):
        if(members and len(members)>=1 and gId):
            try:
                groupInfo = GcGroups.objects.get(id=gId,user_id=userId);   
                GcGroupMembers.objects.filter(gc_group_id=gId,member_id__in=members).delete();
                return {'statusCode':0,"status":
                     "Members have been removed successfully"};
            except GcGroups.DoesNotExist:
                    return {'statusCode':4,
                    'status':"Group not found please check and try again"};
            
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};

class GroupCampaigns(models.Model):
    gc_group = models.ForeignKey('group.GcGroups',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    class Meta(object):
        unique_together=[
        ['gc_group','campaign']
        ]

    def assignNewCampaigns(userId,gId,campaigns,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           campaigns =  json.loads(campaigns);
           return GroupCampaigns.addCampaign(userId,gId,campaigns);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};


    def addCampaign(userId,gId,campaigns):
        if(gId and int(gId)>=1 and campaigns and len(campaigns)>=1):
            #check group info
            try:
                groupInfo = GcGroups.objects.get(id=gId,user_id=userId);
                #check for campaigns (provided campaigns must be user uploaded)
                multipleCampaigns = Multiple_campaign_upload.objects.filter(
                    id__in=campaigns,campaign_uploaded_by=userId);
                multipleCampaignLength = len(multipleCampaigns);

                if(multipleCampaignLength == len(campaigns)):
                    #prepare object to bulk insert
                    gcGroupCampaignsBulk = [];
                    for campaignId in campaigns:
                        gcGroupCampaignsBulk.append(
                            GroupCampaigns(gc_group_id=gId,campaign_id=campaignId));

                    GroupCampaigns.objects.bulk_create(gcGroupCampaignsBulk);
                    return {'statusCode':0,'status':
                    'Campaigns have been assigned successfully'};
                else:
                    return {'statusCode':5,'status':
                    'Some of the campaigns are not found, please refresh and try again later'};
            except GcGroups.DoesNotExist:
                return {'statusCode':4,
                'status':"Group not found please check and try again"};
            return {'campaigns':campaigns};
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};
    
    def removeCampaigns(userId,gId,campaigns,isWeb):
        if(isWeb == False):
            userId = User_unique_id.getUserId(userId);
            if(userId == False):
                return {'statusCode':1,'status':
                "Invalid session, please login"};
        
        try:
           campaigns =  json.loads(campaigns);
           return GroupCampaigns.checkAndRemoveCampaign(userId,gId,campaigns);
           
        except ValueError as ex:
            return {'statusCode':3,'status':
                "Invalid request parameters, campaigns should not be zero - "+str(ex)};
        
        except IntegrityError as e:
            return {'statusCode':5,'status':
            "Group has already some of the campaigns provided, please check and add again"};

        except Exception as e:
            return {'statusCode':3,'status':
                "Invalid request parameters --"+str(e)};

    def checkAndRemoveCampaign(userId,gId,campaigns):
        if(gId and int(gId)>=1 and campaigns and len(campaigns)>=1):
            #check group info
            try:
                groupInfo = GcGroups.objects.get(id=gId,user_id=userId);   
                GroupCampaigns.objects.filter(gc_group_id=gId,campaign_id__in=campaigns).delete()
                return {'statusCode':0,'status':
                    'Campaigns have been removed successfully'};
                
            except GcGroups.DoesNotExist:
                return {'statusCode':4,
                'status':"Group not found please check and try again"};
            return {'campaigns':campaigns};
        else:
            return {'statusCode':3,'status':
                "Invalid request parameters"};