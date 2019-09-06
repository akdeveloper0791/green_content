from django.shortcuts import render

# Create your views here.
from .models import Content
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(["POST"])
def initContentUpload(request):
    if(request.method == "POST"):
        #check the request whether from web or app
        accessToken = request.POST.get('accessToken');
        storeLocation = 2;#default dropbox
        if 'store_location' in request.POST:
            storeLocation = request.POST.get('store_location');
        
        isWeb=False;
        userEmailId=False;
        if(accessToken == "web"):
            isWeb = True
            if request.user.is_authenticated:
                accessToken=request.user.id;
                userEmailId = request.user.email;
            else:
               return JsonResponse({'statusCode':2,
                    'status':'Invalid session, please login'});
        
        response = Content.initUpload(request.POST,
                    accessToken,storeLocation,isWeb,userEmailId);
        return JsonResponse(response);
    else :
        return JsonResponse({'statusCode':1,
            'status':"Invalid request"});

from signagecms import constants
from django.core.files.storage import FileSystemStorage
@api_view(['POST'])
def uploadContentResource(request):
    if(request.method != "POST"):
        return JsonResponse({'statusCode':1,'status':'Invalid method'})
    else:
        requestParams = request.POST;
        accessToken = requestParams.get('access_token');
        isWeb = False;
        if(accessToken == 'web'):
            if(request.user.is_authenticated):
                accessToken = request.user.id
                isWeb = True;
            else:
                return JsonResponse({'statusCode':2,'status':'Invalid access token, please login and try again later'})

        if('file' not in request.FILES):
            return JsonResponse({'statusCode':3,'status':'Invalid request'})
        
        canUpload = (Content.canUploadContentResource(accessToken,requestParams.get('c_id'),isWeb));
        if(canUpload['statusCode']==0):
            #check for file
            saveFile = request.FILES['file'];
            saveFileName = requestParams.get('file_name');
            path = str(constants.file_storage_path)+canUpload['content'].file_path;
            fs = FileSystemStorage(location=path);
            fileFound = True;saveResponse=True;
            if(fs.exists(saveFileName)==False):
                fileFound = False;
                saveResponse = fs.save(saveFileName, saveFile)
                if(saveResponse==saveFileName):
                   saveResponse=True;
                else:
                    saveResponse=False;
            
            if(saveResponse==True):
                return JsonResponse({'statusCode':0,'status':'can upload','path':path,'fileFound':fileFound,'saveResponse':saveResponse})
            else:
                return JsonResponse({'statusCode':4,'status':'unable to upload the file , please try again later'})
                    
        else:
            return JsonResponse({'statusCode':3,'status':canUpload['status']});