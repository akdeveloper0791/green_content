from django.shortcuts import render
from django.contrib.auth import  authenticate
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse
from cmsapp.models import User_unique_id
from signagecms import constants
from .models import Player, Metrics
from django.core.files.storage import FileSystemStorage

# Create your views here.
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
            if(postParams.get('isAdskite') and postParams.get('isAdskite')=='true'):
                if(pwd==constants.ADSKITE_PLAYER_REGISTER_PWD):
                    isLogin=True;
            else:
                isAuthenticated = authenticate(request,username=userEmail,password=pwd)
                if(isAuthenticated is not None):
                    isLogin=True;

            if(isLogin):
                userInfo={};userId=None;
                for info in user:
                    userInfo["user_unique_key"]=User_unique_id.getUniqueKey(info.id)
                    userInfo["first_name"] = info.first_name
                    userInfo["last_name"] = info.last_name
                    userInfo["email"] = info.username
                    userId = info.id;
                    break;
                result = Player.registerPlayer(postParams.get('data'),userId);
                if(result['statusCode']==0):
                    return JsonResponse({'statusCode':0,'status':'Success','info':userInfo,'d_status':result['status'],'player':result['player'],
                        'mac':result['mac']});
                else:
                    return JsonResponse(result);
            else:
                return JsonResponse({'statusCode':3,'status':'Invalid password, please enter valid password'});

        else:
            return JsonResponse({'statusCode':2,'status':
                'Invalid user info, no user found with the email, please register','userEmail':request.POST.get('user_email')})

@api_view(['POST'])
def metrics(request):    
    if('file' in request.FILES):
        player = request.POST.get('player');
        fileObj = request.FILES['file'];
        #folder='C:/Users/Jitendra/python_projects/greencontent/media/player_metrics/{}'.format(str(player))
        folder='/home/adskite/myproject/signagecms/media/player_metrics/{}'.format(str(player))
        fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT
        saveResponse = fs.save(fileObj.name, fileObj)
        file_location = '/player_metrics/{}/{}'.format(str(player),fs);
        response = Metrics.saveRec(player,file_location);
        if(response==False):
            fs.delete(saveResponse);
            return JsonResponse({'statusCode':1,'status':'Invalid player'})
        return JsonResponse({'files':fileObj.size,'saveResponse':saveResponse})

    return JsonResponse({'status':"Invalid file"})

@api_view(['POST'])
def refreshFCM(request):
    if(request.method != 'POST'):
        return JsonResponse({'statusCode':1,'status':
            'Invalid method'});
    else:
        params = request.POST;
        result = Player.refreshFCM(params.get('player'),
            params.get('p_mac'),params.get('fcm'));
        if(result==True):
            return JsonResponse({'statusCode':0,
                'status':'Updated successfully'});
        else:
            return JsonResponse({'statusCode':0,
                'status':'Invalid details'});