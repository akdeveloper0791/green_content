from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import GcGroups,GroupCampaigns,GcGroupMembers
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def gcGroups(request):
    if(request.user.is_authenticated):
        groups = GcGroups.listGroups(request.user.id,True);
    return render(request,'groups/gc_groups.html',{'res':groups});

@api_view(['POST'])
def createGroupApi(request):
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
        
        response = GcGroups.createGroup(accessToken,
            request.POST.get('members'),isWeb,request.POST.get('name'));
        
        return JsonResponse(response);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def groupInfo(request):
    if(request.method == 'POST'):
        accessToken = request.POST.get('accessToken');
        isWeb = False;
        if(accessToken == 'web'):
            if(request.user.is_authenticated):
                accessToken = request.user.id;
                isWeb = True;
            else:
                return JsonResponse({'statusCode':2,
                    'status':"Invalid accessToken, please login"});

        response = GcGroups.getGroupInfo(accessToken,
            request.POST.get('gId'),isWeb);
        return JsonResponse(response);
        
    else:
        return JsonResponse({'statusCode':
            1,'status':'Invalid method'})

@api_view(['POST'])
def assignCampaigns(request):
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
        
        result = GroupCampaigns.assignNewCampaigns(
            accessToken,request.POST.get('gId'),
            request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def removeCampaigns(request):
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
        
        result = GroupCampaigns.removeCampaigns(
            accessToken,request.POST.get('gId'),
            request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def assignMembers(request):
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
        
        result = GcGroupMembers.assignNewMembers(
            accessToken,request.POST.get('gId'),
            request.POST.get('members'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def removeMembers(request):
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
        
        result = GcGroupMembers.removeMembers(
            accessToken,request.POST.get('gId'),
            request.POST.get('members'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def getAssignedGroups(request):
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
        
        result = GcGroupMembers.getAssignedGroups(
            accessToken,isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def updateMemberGroupStatus(request):
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
        
        result = GcGroupMembers.updateMemberGroupStatus(
            accessToken,request.POST.get('g_id'),request.POST.get('status'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});