from django.shortcuts import render
from django.contrib.auth import  authenticate
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse
from cmsapp.models import User_unique_id
from signagecms import constants
from .models import Player, Age_Geder_Metrics, Last_Seen_Metrics
from django.core.files.storage import FileSystemStorage
import numpy as np
import cv2
from django.contrib.auth.decorators import login_required
from campaign.models import Player_Campaign

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
                    #save last seen metrics
                    Last_Seen_Metrics.saveMetrics(result['player']);
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
        #save auto sync metrics
        Last_Seen_Metrics.saveMetrics(player);

        #Init open cv DNN(age and gender) and cascades(face detetion)
        #server path --> /home/adskite/myproject/signagecms/
        #local path --> C:/Users/Jitendra/python_projects/green_content
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

@login_required
def deviceMgmt(request):
    if(request.user.is_authenticated==False):
        return render('/signin/');
    else:
        #get auto sync metrics
        metrics = Last_Seen_Metrics.getMetrics(request.user.id);
        return render(request,'player/device_mgmt.html',{'res':metrics})
        return JsonResponse(metrics);


@api_view(['POST'])
def groupCampaingsInfo(request):
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

        response = Player_Campaign.getCampaignsInfo(accessToken,
            request.POST.get('pId'),isWeb);
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
        
        result = Player_Campaign.assignNewCampaigns(
            accessToken,request.POST.get('pId'),
            request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def assignCampaignsToPlayer(request):
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
        
        result = Player_Campaign.assignCampaignsToPlayers(
            accessToken,request.POST.get('players'),
            request.POST.get('campaignId'),isWeb);

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
        
        result = Player_Campaign.removeCampaigns(
            accessToken,request.POST.get('pId'),
            request.POST.get('campaigns'),isWeb);

        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid method'});

@api_view(['POST'])
def getPlayerCampaigns(request):
    if(request.method == 'POST'):
        player = request.POST.get('player');
        result = Player_Campaign.getPlayerCampaignsWithInfo(player,request.POST.get("secretKey"));
        
        #save auto sync metrics
        Last_Seen_Metrics.saveMetrics(player);
        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

@api_view(['POST'])
def getSchedulePlayerCampaigns(request):
    if(request.method == 'POST'):
        player = request.POST.get('player');
        result = Player_Campaign.getPlayerScheduleCampaignsWithInfo(player,request.POST.get("secretKey"));
        
        #save auto sync metrics
        Last_Seen_Metrics.saveMetrics(player);
        return JsonResponse(result);
        
    else:
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

from .models import Campaign_Reports
@api_view(['POST'])
def saveCampaignReports(request):
    if(request.method=="POST"):
        postParams = request.POST;
        if('player' in postParams and 'p_mac' in postParams and 
            'data' in postParams):
            response = Campaign_Reports.saveCampaignReports(postParams.get('player'),
                postParams.get('p_mac'),postParams.get('data'));
            return JsonResponse(response);
        else:
            return JsonResponse({'statusCode':1,'status':"Invalid request"})
    else:
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

@api_view(['POST'])
def getCampaignReports(request):   
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

@login_required
def campaignReports(request):
    if request.user.is_authenticated:
        devices = Player.getMyPlayers(request.user.id);
        return render(request,'player/campaign_reports.html',{'devices':devices})
    else:
        return render(request,'signin.html');


@api_view(['POST'])
def exportCampaignReports(request):   
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
            result = Campaign_Reports.getCampaignReports(secretKey,isUserId,postParams,True);
            if(result['statusCode']==0):
                return exportCampaignReportsToExcel(result['metrics']);
            else:
                return exportCampaignReportsToExcel(False);
        else:
          return JsonResponse({'statusCode':6,
            'status':'No data available'})

from django.http import HttpResponse
import xlsxwriter
from datetime import timedelta
import uuid 
import time

def exportCampaignReportsToExcel(metrics):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output);
    worksheet = workbook.add_worksheet();
    cell_format = workbook.add_format()
    cell_format.set_align("center");
    cell_format.set_align('vcenter')

    worksheet.set_column('A:E', 25)
    if(metrics==False):
        worksheet.set_header("No reports found");
        worksheet.set_column('A:A', 50)
        worksheet.write('A1', "No reports found")
    else:   
        coloumn_names = ['Device Name', 'Campaign', 'Number Of times played', 'Total duration(Sec)','Last played at'] 
        row=0;coloumn=0;
        for coloumnName in coloumn_names:
            worksheet.write(row,coloumn,coloumnName,cell_format);
            coloumn += 1;
       
        #add data
        row=1;coloumn=0;
        for report in metrics:
            coloumn=0;
            for value in (report):
                if(coloumn==4):#date value
                    value = value.replace(tzinfo=None)
                    value = value + timedelta(minutes=330)#add indian time zone
                    date_format = workbook.add_format({'num_format': 'dd/mm/yy HH:mm:ss'})
                    date_format.set_align("center");
                    date_format.set_align('vcenter');
                    worksheet.write(row, coloumn,value,date_format);
                else:
                    worksheet.write(row, coloumn,value,cell_format);
                coloumn +=1;
            row +=1;


    workbook.close() 
    output.seek(0);

    

    filename = 'Campaign_Reports_{}.xlsx'.format(str(round(time.time() * 1000))+uuid.uuid4().hex[:6]);

    response = HttpResponse(
             (output),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response;

import csv
def exportCampaignReportsToCsv(metrics):
     response = HttpResponse(content_type='text/csv')
     response['Content-Disposition'] = 'attachment; filename="campaign_reports.csv"'

     writer = csv.writer(response)
     writer.writerow(['Device Name', 'Campaign', 'Number Of times played', 'Total duration(Sec)','Last played at'])
     for report in metrics:
        
        writer.writerow([report['player__name'],report['campaign_name'],
            report['t_played'],report['t_duration'],report['last_played_at']]);

     return response;

@api_view(['POST'])
def exportViewerMetrics(request):   
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
            result = Age_Geder_Metrics.getViewerMetrics(secretKey,isUserId,postParams,True);
            if(result['statusCode']==0):
               return prepareViewerMetricsExcel(result['metrics']);
            else:
                return prepareViewerMetricsExcel(False);
        else:
          return JsonResponse({'statusCode':6,
            'status':'No data available'})

import xlsxwriter
import io

def prepareViewerMetricsExcel(metrics):
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output);
    worksheet = workbook.add_worksheet();
    cell_format = workbook.add_format()
    cell_format.set_align("center");
    cell_format.set_align('vcenter');

    worksheet.set_column('A:L', 25)
    if(metrics==False):
        worksheet.set_header("No reports found");
        worksheet.set_column('A:A', 50)
        worksheet.write('A1', "No reports found")
    else:   
        coloumn_names = ['Device Name', 'Date & Time', 'Male', 'Female','Age (0-2)',
            'Age (4-6)','Age (8-12)','Age (15-20)','Age (25-32)',
            'Age (38-43)','Age (48-53)','Age (60-100)'] 
        row=0;coloumn=0;
        for coloumnName in coloumn_names:
            worksheet.write(row,coloumn,coloumnName,cell_format);
            coloumn += 1;
       
        #add data
        row=1;coloumn=0;
        for report in metrics:
            coloumn=0;
            for value in (report):
                if(coloumn==1):#date value
                    naive_datetime = value.replace(tzinfo=None)
                    naive_datetime = naive_datetime + timedelta(minutes=330)#add indian time zone
                    date_format = workbook.add_format({'num_format': 'dd/mm/yy HH:mm:ss'})
                    date_format.set_align("center");
                    date_format.set_align('vcenter');
                    worksheet.write(row, coloumn,naive_datetime,date_format);
                else:
                    worksheet.write(row, coloumn,value,cell_format);
                coloumn +=1;
            row +=1;


    workbook.close() 
    output.seek(0);

    

    filename = 'viewer_metrics_{}.xlsx'.format(str(round(time.time() * 1000))+uuid.uuid4().hex[:6]);
    response = HttpResponse(
             (output),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response;



def prepareViewerMetricsCsv(metrics):
     response = HttpResponse(content_type='text/csv')
     response['Content-Disposition'] = 'attachment; filename="viewer_metrics.csv"'

     writer = csv.writer(response)
     writer.writerow(['Device Name', 'Date & Time', 'Male', 'Female','Age (0-2)',
        'Age (4-6)','Age (8-12)','Age (15-20)','Age (25-32)',
        'Age (38-43)','Age (48-53)','Age (60-100)'])
     for report in metrics:
        writer.writerow(report)
        '''writer.writerow([report['player__name'],report['created_at'],
            report['g_male'],report['g_female'],report['age_0_2'],
            report['age_4_6'],report['age_8_12'],report['age_15_20'],
            report['age_25_32'],report['age_38_43'],report['age_48_53'],report['age_60_100']]);'''

     return response;


@login_required
def playerGroup(request):
    if(request.user.is_authenticated==False):
        return render('/signin/');
    else:
        return render(request,'player/player_group.html')

@api_view(["POST"])
def listPlayersToPublishCamp(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            response = Player.listPlayersToPublishCamp(
                request.POST.get('cId'),request.user.id);

            return JsonResponse(response);

        else:
            return JsonResponse({'statusCode':1,'status':'Session has been expired, please relogin'});
    else:
        return JsonResponse({'statusCode':1,'status':'Invalid method'});

from campaign.models import CampaignInfo,Schedule_Campaign
@login_required
def scheduleCampaign(request,player,campaign): 
    playerCampaign = Player_Campaign.getPlayerCampaign(player,campaign,request.user.id);
    if(playerCampaign==False):
        return render(request,'player/schedule_campaign.html',{'status':False,'error':'Invalid campaign, info not found'});
    
    playerInfo = Player.isMyPlayer(player,request.user.id);
    if(playerInfo==False):
        return render(request,'player/schedule_campaign.html',{'status':False,'error':'Invalid player, player details not found'});
    
    campaignInfo = CampaignInfo.getPreviewCampaignInfo(request.user.id,campaign);
    if(campaignInfo['statusCode']!=0):
        return render(request,'player/schedule_campaign.html',{'status':False,'error':campaignInfo['status']});
    
    schedules = Schedule_Campaign.getPCSchedules(playerCampaign.id);
    return render(request,'player/schedule_campaign.html',{'status':True,'pc_id':playerCampaign.id,'schedules':schedules,'player_name':playerInfo.name,
        'camapaign_name':campaignInfo['c_name']});
    