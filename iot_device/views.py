from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .models import IOT_Device, Contextual_Ads_Rule, CAR_Campaign, CAR_Device
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate
from django.http import JsonResponse

# Create your views here.
@login_required
def contextualAdsRules(request):
    if request.user.is_authenticated:
        devices = IOT_Device.getMyPlayers(request.user.id);
        return render(request,'iot_device/contextual_ad_rules.html',{'devices':devices});
    else:
        return render(request,'signin.html');

@api_view(['POST'])
def register(request):
    if(request.method!='POST'):
        return JsonResponse({'statusCode':1,
            'status':'Invalid request'});
    else:
        postParams = request.POST;
        userEmail = postParams.get('user_email');
        user = User.objects.filter(username= userEmail)
        pwd = postParams.get('pwd');
        if user:
            isLogin=False;
            isAuthenticated = authenticate(request,username=userEmail,password=pwd)
            if(isAuthenticated is not None):
                isLogin=True;

            if(isLogin):
                userInfo={};userId=None;
                for info in user:
                    userId = info.id;
                    break;
                result = IOT_Device.registerPlayer(postParams.get('data'),userId);
                if(result['statusCode']==0):
                    return JsonResponse({'statusCode':0,'status':'Success','iot':result['player'],
                        'mac':result['mac'],'key':result['key']});
                else:
                    return JsonResponse(result);
            else:
                return JsonResponse({'statusCode':3,'status':'Invalid password, please enter valid password'});

        else:
            return JsonResponse({'statusCode':2,'status':
                'Invalid user info, no user found with the email, please register','userEmail':request.POST.get('user_email')})

@api_view(["POST"])
def createRule(request):
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
        
        result = Contextual_Ads_Rule.createRule(request.POST.get('iot_device'),
            accessToken,request.POST.get('players'),
            request.POST.get('campaigns'),request.POST.get('classifier'),request.POST.get('delay_time'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(["POST"])
def deleteRule(request):
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
        
        result = Contextual_Ads_Rule.deleteRule(request.POST.get('rule_id'),
            accessToken,isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(["POST"])
def assignCampaignsToCARule(request):
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
        
        result = CAR_Campaign.assignNew(request.POST.get('rule_id'),
            accessToken,request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(["POST"])
def removeCampaignsFromCARule(request):
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
        
        result = CAR_Campaign.remove(request.POST.get('rule_id'),
            accessToken,request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(["POST"])
def assignDevicesToRule(request):
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
        
        result = CAR_Device.assignNew(request.POST.get('rule_id'),
            accessToken,request.POST.get('players'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(["POST"])
def removeDevicesFromRule(request):
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
        
        result = CAR_Device.remove(request.POST.get('rule_id'),
            accessToken,request.POST.get('players'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});
