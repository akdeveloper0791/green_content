from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from cmsapp.models import Multiple_campaign_upload,User_unique_id
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import CampaignInfo,Approved_Group_Campaigns
import json
from group.models import GroupCampaigns
from player.models import Last_Seen_Metrics;

# Create your views here.
@login_required
def upload_camp_web(request):
    if request.method == "POST":
        #fileObj = request.FILES['file']
        campaigns = Multiple_campaign_upload.objects.filter();
        campaigns = list(campaigns);
        return JsonResponse({'file':'fileObj.size'})
    else:
        return render(request,'campaign/upload_file.html')

'''
 1->Invalid request
 2->Invalid session, please login
 3->Unable to save the campaign
 '''
@api_view(['GET','POST'])
def initCampaignUpload(request):
    if(request.method == "POST" and
     'campaign' in request.POST and 'size' in request.POST):
        #check the request whether from web or app
        accessToken = request.POST.get('accessToken');
        if(accessToken == "web"):
            if request.user.is_authenticated:
                response = CampaignInfo.processInfoAndSaveCampaign(request.POST.get('info'),
                    accessToken,request.user.id,
                    request.POST.get('campaign'),request.POST.get('size'));
                return JsonResponse(response);
            else:
               return JsonResponse({'statusCode':2,
                    'status':'Invalid session, please login'});
        else:
            response = CampaignInfo.processInfoAndSaveCampaign(request.POST.get('info'),
                    "api",accessToken,request.POST.get('campaign'),request.POST.get('size'));
            return JsonResponse(response);
    else :
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

@login_required
def listCampaignsWeb(request):
    if request.user.is_authenticated:
        response = CampaignInfo.getUserCampaignsWithInfo(request.user.id,True);
        #get access token
        secretKey = User_unique_id.getUniqueKey(request.user.id);
        return render(request,'campaign/list.html',{'res':response,
            'secretKey':secretKey});
    else:
        return JsonResponse({'statusCode':2,
                    'status':'Invalid session, please login'});

@api_view(['POST'])
def listMyCampaignsAPI(request):
    if(request.method == 'POST'):
        isUserId = False;
        secretKey = request.POST.get("secretKey")
        if(secretKey=='web'):
            isUserId = True;
            if(request.user.is_authenticated):
                secretKey = request.user.id;
            else:
                return JsonResponse(
                    {'statusCode':2,'status':"Invalid accessToken please login"});
        result = CampaignInfo.getUserCampaignsWithInfo(secretKey,isUserId);
        if(request.POST.get('player')):
            #save auto sync metrics
            Last_Seen_Metrics.saveMetrics(request.POST.get('player'));
        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});
        
@api_view(['POST'])
def deleteMyCampaign(request):
    if(request.method == 'POST'):
        isWeb = False;
        accessToken = request.POST.get('accessToken');
        if(accessToken=="web"):
            if(request.user.is_authenticated):
                accessToken=request.user.id;
                isWeb=True;
            else:
                return JsonResponse({'statusCode':200,
            'status':'Invalid session'});

        result = CampaignInfo.deleteMyCampaign(request.POST.get('camp_id'),
            accessToken,request.POST.get('mac'),isWeb);
        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid request'});

@api_view(['POST','GET'])
def listCampaigns1(request):
    result = CampaignInfo.listCampaigns1();
    return JsonResponse(result);

@api_view(['POST'])
def updateSavePath(request):
    result = CampaignInfo.updateSavePath(request.POST.get('userId'),
        request.POST.get('accessToken'));
    return JsonResponse(result);

@api_view(['POST'])
def removeApprovedCampaign(request):
    if(request.method == 'POST'):
        isWeb = False;
        accessToken = request.POST.get('accessToken');
        if(accessToken == 'web'):
            if(request.user.is_authenticated):
                accessToken = request.user.id;
                isWeb = True;
            else:
                return JsonResponse({'status':2,
                    'status':"Invalid accessToken please login and try"});
        
        result = Approved_Group_Campaigns.removeApprovedCampaign(
            accessToken,request.POST.get('rec_id'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});


def previewCampaign(request,c_id):
    if(request.user.is_authenticated):
        if(request.method=='GET'):
            info = CampaignInfo.getPreviewCampaignInfo(request.user.id,c_id);
        else:
            info = {"statusCode":1,"status":"Invalid method"};
    else:
        info = {"statusCode":1,"status":"Invalid access token please login and try"};

    return render(request,'campaign/preview_campaign.html',{"info":json.dumps(info)});

@login_required
def create(request):
    return render(request,'campaign/create.html');

@login_required
#two - group id , #one- campaign id
def approveCampaignNotif(request,one,two):
    if(request.user.is_authenticated):
        gCampId = GroupCampaigns.getGroupCampaignKey(two,one);
        if(gCampId==False):
            result = {'statusCode':2,'status':"Invalid details"};
        else:
            result = GroupCampaigns.approveGroupCampaign(
                request.user.id,gCampId,True);
        #return JsonResponse(result);
        return render(request,'groups/approve_member_email.html',{'res':result});
    else:
        return JsonResponse({'statusCode':1,'status':'Please login'});