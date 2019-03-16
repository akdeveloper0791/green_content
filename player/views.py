from django.shortcuts import render
from django.contrib.auth import  authenticate
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse
from cmsapp.models import User_unique_id
from signagecms import constants
from .models import Player, Age_Geder_Metrics
from django.core.files.storage import FileSystemStorage
import numpy as np
import cv2
from django.contrib.auth.decorators import login_required

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
                        'mac':result['mac'],'fcm':result['fcm']});
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
     player = Player.getPlayer(request.POST.get('player'),request.POST.get('p_mac'))
     if(player!=False):
        #Init open cv DNN(age and gender) and cascades(face detetion)
        face_detector = "/home/adskite/myproject/signagecms/haarcascade_frontalface_alt.xml"
        age_net = cv2.dnn.readNetFromCaffe(
                        "/home/adskite/myproject/signagecms/age_gender_model/deploy_age.prototxt", 
                        "/home/adskite/myproject/signagecms/age_gender_model/age_net.caffemodel")

        gender_net = cv2.dnn.readNetFromCaffe(
                        "/home/adskite/myproject/signagecms/age_gender_model/deploy_gender.prototxt", 
                        "/home/adskite/myproject/signagecms/age_gender_model/gender_net.caffemodel")

        player = request.POST.get('player');
        fileObj = request.FILES['file'];
        
        #detect face 
        image_to_read = read_cv_image(stream = fileObj)
        
        #raw image to detect age and gender
        image = image_to_read

        image_to_read = cv2.cvtColor(image_to_read, cv2.COLOR_BGR2GRAY)
        detector_value = cv2.CascadeClassifier(face_detector)
        faces = detector_value.detectMultiScale(image_to_read,1.1,5);
        
        #detect age and gender
        ages = {};
        age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        gender_list = ['Male', 'Female']
        genders = {};
        if len(faces)>=1:
            for (x,y,w,h) in faces:        
                face_img = image[y:y+h, x:x+w].copy()
                blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                # Predict gender
                gender_net.setInput(blob)
                gender_preds = gender_net.forward()
                gender = gender_list[gender_preds[0].argmax()]
                if gender in genders:
                    genders[gender] = genders[gender]+1;
                else:
                    genders[gender]=1;
                # Predict age
                age_net.setInput(blob)
                age_preds = age_net.forward()
                #age = age_list[age_preds[0].argmax()]
                age=str(age_preds[0].argmax());
                #overlay_text = "%s, %s" % (gender, age)
                #cv2.putText(image, overlay_text ,(x,y), font, 2,(255,255,255),2,cv2.LINE_AA)
                if age in ages:
                    ages[age]=ages[age]+1;
                else:
                    ages[age]=1
            

            '''#folder='C:/Users/Jitendra/python_projects/greencontent/media/player_metrics/{}'.format(str(player))
            folder='/home/adskite/myproject/signagecms/media/player_metrics/{}'.format(str(player))
            fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT
            #saveResponse = fs.save(fileObj.name, fileObj)
            file_location = '/player_metrics/{}/{}'.format(str(player),fs);'''
            response = Age_Geder_Metrics.saveMetrics(player,genders,ages);
            if(response['statusCode']==0):
                  
                return JsonResponse({'statusCode':0,'faces':len(faces),
                'ages':(ages),'genders':genders})
            else:
                #fs.delete(saveResponse);
                return JsonResponse({'statusCode':5,
                    'status':response['status']})
        else:
            return JsonResponse({'statusCode':6,'status':'No faces detected'})
     else:
        return JsonResponse({'statusCode':1,'status':'Invalid player'})

    return JsonResponse({'statusCode':2,'status':"Invalid file"})

def read_cv_image(path=None, stream=None, url=None):

    ##### primarily URL but if the path is None
    ## load the image from your local repository

    if path is not None:
        image = cv2.imread(path)

    else:
        if url is not None:

            response = urllib.request.urlopen(url)

            data_temp = response.read()

        elif stream is not None:
            #implying image is now streaming
            data_temp = stream.read()

        image = np.asarray(bytearray(data_temp), dtype="uint8")

        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

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

@login_required
def viewerMetrics(request):
    if request.user.is_authenticated:
        devices = Player.getMyPlayers(request.user.id);
        return render(request,'player/viewer_metrics.html',{'devices':devices})
    else:
        return render(request,'signin.html');

@api_view(['POST'])
def getViewerMetrics(request):   
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
            result = Age_Geder_Metrics.getViewerMetrics(secretKey,isUserId,postParams);
            return JsonResponse(result); 
        else:
          return JsonResponse({'statusCode':6,
            'status':'No data available'})   