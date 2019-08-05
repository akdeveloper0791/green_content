from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Device_Group, Device_Group_Player, Device_Group_Campaign
from django.http import JsonResponse

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

def deviceGroups(request):
    groups = Device_Group.getMyGroups(request.user.id);
    return render(request,'device_group/device_groups.html',{'groups':groups});

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