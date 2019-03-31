from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Device_Group, Device_Group_Player
from django.http import JsonResponse

# Create your views here.
@api_view(['POST'])
def create(request):
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
def assignPlayers(request):
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
def removePlayers(request):
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
