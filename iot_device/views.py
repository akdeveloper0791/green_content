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


@api_view(['POST'])
def getCARules(request):   
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
            
        result = IOT_Device.getContextualAdRules(secretKey,isUserId,postParams.get('iot_device'));
        return JsonResponse(result); 

@api_view(['POST'])
def getCARuleInfo(request):   
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
            
        result = IOT_Device.getContextualAdRuleInfo(secretKey,isUserId,postParams.get('rule_id'),
            ('is_campaigns' in postParams),('is_devices' in postParams));
        return JsonResponse(result);

from signagecms import constants
import numpy as np
import cv2
from .models import Age_Geder_Metrics

@api_view(['POST'])
def metrics(request):    
    if('file' in request.FILES):
     player = IOT_Device.getPlayer(request.POST.get('player'),request.POST.get('p_key'))
     if(player!=False):
        
        #Init open cv DNN(age and gender) and cascades(face detetion)
        #server path --> /home/adskite/myproject/signagecms/
        #local path --> C:/Users/Jitendra/python_projects/green_content
        pathToLib = constants.project_server_path;
        if(constants.setup == 1):
            pathToLib = constants.project_local_path;

        face_detector = "{}/haarcascade_frontalface_alt.xml".format(pathToLib)
        age_net = cv2.dnn.readNetFromCaffe(
                        "{}/age_gender_model/deploy_age.prototxt".format(pathToLib), 
                        "{}/age_gender_model/age_net.caffemodel".format(pathToLib))

        gender_net = cv2.dnn.readNetFromCaffe(
                        "{}/age_gender_model/deploy_gender.prototxt".format(pathToLib), 
                        "{}/age_gender_model/gender_net.caffemodel".format(pathToLib))

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
                #calculate player auto campaign rule
                auto_campaign_rule = calculateAutoCampaignRule(ages,genders,faces);  
                return JsonResponse({'statusCode':0,'faces':len(faces),
                'ages':(ages),'genders':genders,'rule':auto_campaign_rule})
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

def calculateAutoCampaignRule(ages,genders,faces):
    if("Male" in genders and genders['Male']==len(faces)):
        return "male";
    elif("Female" in genders and genders['Female']==len(faces)):
        return "woman";
    elif(len(faces)==2 and "Female" in genders and "Male" in genders):
        #check for couples
        gender_pos=0;femaleAge=0;maleAge=0;
        for gender in genders:
            age_pos=0;
            if(len(ages)==2):
                for age in ages:
                    if(age_pos == gender_pos):
                        if(gender == "Female"):
                            femaleAge = age;
                        elif(gender=="Male"):
                            maleAge = age;
                        break;
                    age_pos= age_pos+1;
                gender_pos = gender_pos+1;
            else:
               for age in ages:
                 femaleAge=age;
                 maleAge=age; 
            

        
        femaleAgeInt = int(femaleAge);
        maleAgeInt = int(maleAge);
        
        if(femaleAgeInt >= 3 and (maleAgeInt==femaleAgeInt)):
            return "family";
        else:
            return "family";
    else:
        return "family";