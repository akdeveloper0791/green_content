from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import License_Device
# Create your views here.
@api_view(['POST'])
def licenseRegister(request):
    if(request.method!='POST'):
        return JsonResponse({'statusCode':1,
            'status':'Invalid request'});
    else:
        postParams = request.POST;
        result = License_Device.registerPlayer(postParams.get('data'));
        if(result['statusCode']==0):    
            return JsonResponse({'statusCode':0,'status':'Success','d_status':result['status'],
                        'mac':result['mac'],'expiry_date':result['expiry_date']});
        else:
            return JsonResponse(result);

import random
import requests
@api_view(["POST"])
def sendOTP(request):
    systemRandom = random.SystemRandom();
    randomOTP = systemRandom.randrange(100000,999999);
    mobileNumberResponse = sendOTPToMobileNumber(request.POST.get("mobile_number"),
        randomOTP);
    
    
    emailResponse = sendOTPToEmail(request.POST.get('email'),randomOTP); 
    return JsonResponse({'statusCode':0,
        'randomOTP':randomOTP,
        'mobileNumberResponse':mobileNumberResponse,
        'emailResponse':emailResponse});

def sendOTPToMobileNumber(mobileNumber,secureOTP):
    getRequest = "http://123.63.33.43/blank/sms/user/urlsmstemp.php?username=adskite_lite_transactional&pass=adsKite123ibetteR$&senderid=ADSKIT&dest_mobileno={}&tempid=51576&F1={}&response=Y".format(mobileNumber,secureOTP);
    response = requests.get(getRequest);
    response = response.text;
    response =response.replace("-","");
    response = response.replace("_","");
    response = response.replace("\n","");
    if(response.isnumeric()):
        return True;
    else:
        return response;
from django.core import mail
from signagecms import constants
def sendOTPToEmail(email,secureOTP):
    try:
        with mail.get_connection() as connection:   
            message = "Your AdsKite one time password is {}".format(secureOTP); 
            to = [email];
            msg = EmailMessage("DSP OTP", message, to=to, from_email=constants.EMAIL_HOST_USER,
                    connection=connection)
            msg.content_subtype = 'text'
            response = msg.send();
            if(response==1):
                return True;
            else:
                return "Error in sending Email OTP ";
    except Exception as e:
        return "Error in sending Email OTP "+str(e)