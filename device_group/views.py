from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Device_Group, Device_Group_Player, Device_Group_Campaign
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@api_view(['POST'])
def createDG(request):
    if(request.method == 'POST'):
        isWeb = False;
        accessToken = request.POST.get('accessToken');
        if(accessToken == "web"):
            if(request.user.is_authenticated):
                accessToken = request.user.id;
                isWeb = True;
            else:
                return JsonResponse({'statusCode':2,
                    'status':'Invalid accessToken please login and try'});
        
        response = Device_Group.createGroup(accessToken,
            request.POST.get('name'),isWeb);
        
        return JsonResponse(response);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(["POST"])
def deleteDG(request):
    if(request.method == 'POST'):
        isWeb = False;
        accessToken = request.POST.get('accessToken');
        if(accessToken == "web"):
            if(request.user.is_authenticated):
                accessToken = request.user.id;
                isWeb = True;
            else:
                return JsonResponse({'statusCode':2,
                    'status':'Invalid accessToken please login and try'});
        response = Device_Group.deleteDG(request.POST.get('dg_id'),accessToken,isWeb);
        return JsonResponse(response);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def assignPlayersDG(request):
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
        
        result = Device_Group_Player.assignNewPlayers(
            accessToken,request.POST.get('gId'),
            request.POST.get('players'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def removePlayersDG(request):
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
        
        result = Device_Group_Player.removePlayers(
            accessToken,request.POST.get('gId'),
            request.POST.get('players'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def assignCampaignsDG(request):
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
        
        result = Device_Group_Campaign.assignNewCampaigns(
            accessToken,request.POST.get('gId'),
            request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def removeCampaignsDG(request):
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
        
        result = Device_Group_Campaign.removeCampaigns(
            accessToken,request.POST.get('gId'),
            request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});


@login_required
def deviceGroups(request):
    groups = Device_Group.getMyGroups(request.user.id);
    response = render(request,'device_group/device_groups.html',{'groups':groups})
   
    response.set_cookie('device_mgmt_last_accessed', 'dg');
    return response;

@api_view(["POST"])
def getDGInfo(request):
    if(request.method == 'POST'):
        postParams = request.POST;
        isUserId = False;
        secretKey = request.POST.get("accessToken")
        if(secretKey=='web'):
            isUserId = True;
            if(request.user.is_authenticated):
                secretKey = request.user.id;
            else:
                return JsonResponse(
                    {'statusCode':2,'status':"Invalid accessToken please login"});
            
        result = Device_Group.getDGInfo(secretKey,isUserId,postParams.get('dg_id'),
            ('is_campaigns' in postParams),('is_devices' in postParams));
        return JsonResponse(result);

from campaign.models import CampaignInfo,Schedule_Campaign

@login_required
def dgScheduleCampaign(request,dg,campaign): 
    deviceGroupCampaign = Device_Group_Campaign.getDGCampaign(dg,campaign,request.user.id);
    if(deviceGroupCampaign==False):
        return render(request,'player/schedule_campaign.html',{'status':False,'error':'Invalid campaign, info not found'});
   
    dgInfo = Device_Group.isMyDeviceGroup(dg,request.user.id);
    if(dgInfo==False):
        return render(request,'player/schedule_campaign.html',{'status':False,'error':'Invalid device group, device group details not found'});
    
    campaignInfo = CampaignInfo.getPreviewCampaignInfo(request.user.id,campaign);
    if(campaignInfo['statusCode']!=0):
        return render(request,'player/schedule_campaign.html',{'status':False,'error':campaignInfo['status']});
    
    schedules = Schedule_Campaign.getDGCSchedules(deviceGroupCampaign.id);
    return render(request,'player/schedule_campaign.html',{'status':True,'pc_id':deviceGroupCampaign.id,'schedules':schedules,'player_name':dgInfo.name,
        'camapaign_name':campaignInfo['c_name'],'type':'dg'});

@api_view(['POST'])
def dgCampaignReports(request):   
    if(request.method == 'POST'):
        postParams = request.POST;
        if(postParams.get('player') and postParams.get('from_date') and postParams.get('to_date')
            and postParams.get('accessToken')):     
            isUserId = False;
            secretKey = request.POST.get("accessToken")
            if(secretKey=='web'):
                isUserId = True;
                if(request.user.is_authenticated):
                    secretKey = request.user.id;
                else:
                    return JsonResponse(
                        {'statusCode':2,'status':"Invalid accessToken please login"});
            result = Campaign_Reports.getCampaignReports(secretKey,isUserId,postParams);
            return JsonResponse(result); 
        else:
          return JsonResponse({'statusCode':6,
            'status':'No data available'})