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
        storeLocation = 2;#default dropbox
        if 'store_location' in request.POST:
            storeLocation = request.POST.get('store_location');

        if(accessToken == "web"):
            if request.user.is_authenticated:
                response = CampaignInfo.processInfoAndSaveCampaign(request.POST.get('info'),
                    accessToken,request.user.id,
                    request.POST.get('campaign'),request.POST.get('size'),storeLocation,
                    request.user.email);
                return JsonResponse(response);
            else:
               return JsonResponse({'statusCode':2,
                    'status':'Invalid session, please login'});
        else:
            response = CampaignInfo.processInfoAndSaveCampaign(request.POST.get('info'),
                    "api",accessToken,request.POST.get('campaign'),request.POST.get('size'),storeLocation,
                    False);
            return JsonResponse(response);
    else :
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

@api_view(["POST"])
def editCampaign(request):
    if(request.method == "POST"):
        #check the request whether from web or app
        accessToken = request.POST.get('accessToken');
        isWeb = False;
        if(accessToken == "web"):
            isWeb=True;
            if request.user.is_authenticated:
                accessToken = request.user.id;    
            else:
               return JsonResponse({'statusCode':2,
                    'status':'Invalid session, please login'});
        
        response = CampaignInfo.editCampaign(request.POST.get('c_id'),
                    accessToken,request.POST,isWeb);
        return JsonResponse(response);
    else :
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

@api_view(["POST"])
def getEditCampaignInfo(request):
    if(request.method == "POST"):
        #check the request whether from web or app
        accessToken = request.POST.get('accessToken');
        isWeb = False;
        if(accessToken == "web"):
            isWeb=True;
            if request.user.is_authenticated:
                accessToken = request.user.id;    
            else:
               return JsonResponse({'statusCode':2,
                    'status':'Invalid session, please login'});
        
        jsResponse = CampaignInfo.getEditCampaignInfo(request.POST.get('c_id'),
                    accessToken,isWeb);
        return JsonResponse(jsResponse);
        return JsonResponse({'statusCode':1,
            'status':"Invalid request123",'id':request.POST.get('c_id')});
    else :
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

@login_required
def listCampaignsWeb(request):
    if request.user.is_authenticated:
        response = CampaignInfo.getCampaignsToDisplayInWeb(request.user.id);
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

from signagecms import constants
from django.core.files.storage import FileSystemStorage
@api_view(['POST'])
def uploadCampaignResource(request):
    if(request.method != "POST"):
        return JsonResponse({'statusCode':1,'status':'Invalid method'})
    else:
        requestParams = request.POST;
        accessToken = requestParams.get('access_token');
        isWeb = False;
        if(accessToken == 'web'):
            if(request.user.is_authenticated):
                accessToken = request.user.id
                isWeb = True;
            else:
                return JsonResponse({'statusCode':2,'status':'Invalid access token, please login and try again later'})

        if('file' not in request.FILES):
            return JsonResponse({'statusCode':3,'status':'Invalid request'})
        
        canUpload = (CampaignInfo.canUploadCampaignResource(accessToken,requestParams.get('c_id'),isWeb));
        if(canUpload['statusCode']==0):
            #check for file
            saveFile = request.FILES['file'];
            saveFileName = requestParams.get('file_name');
            path = str(constants.file_storage_path)+canUpload['campaign'].save_path;
            fs = FileSystemStorage(location=path);
            fileFound = True;saveResponse=True;
            if(fs.exists(saveFileName)==False):
                fileFound = False;
                saveResponse = fs.save(saveFileName, saveFile)
                if(saveResponse==saveFileName):
                   saveResponse=True;
                else:
                    saveResponse=False;
            
            if(saveResponse==True):
                return JsonResponse({'statusCode':0,'status':'can upload','path':path,'fileFound':fileFound,'saveResponse':saveResponse})
            else:
                return JsonResponse({'statusCode':4,'status':'unable to upload the file , please try again later'})
                    
        else:
            return JsonResponse({'statusCode':3,'status':canUpload['status']});

from .models import Schedule_Campaign
@api_view(['GET','POST'])
def saveScheduleCampaign(request):
    if(request.method!="POST"):
        return JsonResponse({'statusCode':1,
            'status':"Invalid method",'request.method':request.method});
    postParams = request.POST;
    isWeb=False;accessToken = postParams.get('access_token');
    if(accessToken=="web"):
        isWeb = True;
        if(request.user.is_authenticated):
            accessToken = request.user.id;
        else:
            return JsonResponse({'statusCode':2,
                'status':'Invalid access token, please login and try'});
    saveResponse=None;
    if('pc_id' in postParams):
        saveResponse = Schedule_Campaign.saveCampaign(isWeb,accessToken,
            postParams.get('schedule_from'),postParams.get('schedule_to'),postParams.get('pc_id'),
            postParams.get('schedule_type'),postParams.get('sc_priority'),postParams.get('additional_info'),
            );
    else:
       saveResponse = Schedule_Campaign.saveDGCSchedule(isWeb,accessToken,
            postParams.get('schedule_from'),postParams.get('schedule_to'),
            postParams.get('schedule_type'),postParams.get('sc_priority'),postParams.get('additional_info'),
            postParams.get('dgc_id')); 
    if(saveResponse['statusCode']==0):
        #schedules = Schedule_Campaign.getPCSchedule(postParams.get('pc_id'),);
        saveResponse['schedules'] = {'id':saveResponse['id'],'schedule_from':postParams.get('schedule_from'),
            'schedule_to':postParams.get('schedule_to'),'schedule_type':postParams.get('schedule_type'),
            'sc_priority':saveResponse['sc_priority'],'additional_info':saveResponse['additional_info']};
    return JsonResponse(saveResponse);

@api_view(['POST'])
def deleteScheduleCampaign(request):
    if(request.method!="POST"):
        return JsonResponse({'statusCode':1,
            'status':"Invalid method",'request.method':request.method});
    postParams = request.POST;
    isWeb=False;accessToken = postParams.get('access_token');
    if(accessToken=="web"):
        isWeb = True;
        if(request.user.is_authenticated):
            accessToken = request.user.id;
        else:
            return JsonResponse({'statusCode':2,
                'status':'Invalid access token, please login and try'});
    deleteResponse = Schedule_Campaign.deleteCampaignSchedule(isWeb,accessToken,
        postParams.get('sc_id'),postParams.get('type'));
    return JsonResponse(deleteResponse);