from django.shortcuts import render
from django.contrib.auth import  authenticate
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse
from cmsapp.models import User_unique_id
from signagecms import constants
from .models import Player
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
                if(result==True):
                    return JsonResponse({'statusCode':0,'status':'Success','info':userInfo,'result':result});
                else:
                    return JsonResponse(result);
            else:
                return JsonResponse({'statusCode':3,'status':'Invalid password, please enter valid password'});

        else:
            return JsonResponse({'statusCode':2,'status':
                'Invalid user info, no user found with the email, please register','userEmail':request.POST.get('user_email')})