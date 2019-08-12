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
        if(postParams.get('groups') and postParams.get('from_date') and postParams.get('to_date')
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
            result = Device_Group_Player.getCampaignReports(secretKey,isUserId,postParams);
            return JsonResponse(result); 
        else:
          return JsonResponse({'statusCode':6,
            'status':'No data available'})

@api_view(["POST"])
def dgExportCampaignReports(request):
    if(request.method == 'POST'):
        postParams = request.POST;
        if(postParams.get('groups') and postParams.get('from_date') and postParams.get('to_date')
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
            result = Device_Group.getCampaignReports(secretKey,isUserId,postParams,True);
            isSendEmail = True if 'emailPartners' in postParams else False

            if(result['statusCode']==0):
                if(isSendEmail):
                    emails = json.loads(postParams.get('emailPartners'));
                    fileName = str(postParams.get('from_date'))+"-"+str(postParams.get('to_date'))+'.xlsx';
                    return exportCampaignReportsToExcel(result['metrics'],emails,fileName);
                else:
                    return exportCampaignReportsToExcel(result['metrics']);
            else:
                if(isSendEmail):
                  return JsonResponse(result);
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

def exportCampaignReportsToExcel(metrics,emails=False,filename = None):
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
        coloumn_names = ['Partner','Device Group', 'Campaign', 'Number Of times played', 'Total duration(Sec)','Last played at'] 
        row=0;coloumn=0;
        for coloumnName in coloumn_names:
            worksheet.write(row,coloumn,coloumnName,cell_format);
            coloumn += 1;
       
        #add data
        row=1;coloumn=0;
        for report in metrics:
            coloumn=0;
            for value in report.values():
                '''if(coloumn==5):#date value
                    #value = value.replace(tzinfo=None)
                    #value = value + timedelta(minutes=330)#add indian time zone
                    date_format = workbook.add_format({'num_format': 'dd/mm/yy HH:mm:ss'})
                    date_format.set_align("center");
                    date_format.set_align('vcenter');
                    worksheet.write(row, coloumn,value,date_format);
                else:
                    worksheet.write(row, coloumn,value,cell_format);'''
                if(coloumn>=6):
                    continue;
                worksheet.write(row, coloumn,value,cell_format);
                coloumn +=1;
            row +=1;

    
    workbook.close() 
    output.seek(0);
    if(filename is None):
        filename = 'Campaign_Reports_{}.xlsx'.format(str(round(time.time() * 1000))+uuid.uuid4().hex[:6]);
    if(emails==False):
        response = HttpResponse(
             (output),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response;
    else:
        emailData = output.read();
        return emailCampaignReports(filename,emailData,emails);

from django.core import mail
from django.core.mail import EmailMessage
from signagecms import constants

def emailCampaignReports(fileName,excelFile,emails):
    try:
        with mail.get_connection() as connection:
            from_email = constants.EMAIL_HOST_USER
            
            msg = EmailMessage("Campaign reports", "Message", to=emails, from_email=from_email,
                        connection=connection);
            msg.content_subtype = 'html'
            msg.attach(fileName, excelFile, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response = msg.send();
            
            return JsonResponse({'statusCode':0,'status':'Reports have been emailed successfully'})
    except Exception as e:
            error = str(e);
            if('10060' in error):
                return JsonResponse({'statusCode':3,'status':'Unable to connect to server, please check yout internet connection'})
            return JsonResponse({'statusCode':3,'status':"Error in sending reports"+str(e)});