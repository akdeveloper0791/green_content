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
                        'mac':result['mac']});
        else:
            return JsonResponse(result);