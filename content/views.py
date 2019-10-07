from django.shortcuts import render

# Create your views here.
from .models import Content
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

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

def mycontent(request):
    return redirect('/content/mycontent/1')

from signagecms.constants import content_pagination_limit
def listMyContent(request,pageNumber):
    if(request.user.is_authenticated):
        totalValues=Content.getTotalContent(request.user.id);
        totalPages= totalValues/content_pagination_limit;
        totalPagesInt = int(totalPages);
        paginationPages=[];
        if(totalPagesInt<totalPages):
            totalPagesInt+=1;
        #Backward,ForwardLimits
        BML,FML,BL,FL=5,5,(pageNumber-1),(totalPagesInt-pageNumber);
        
        if(BL>0 or FL>0):    
            if BL>=5 and FL>=5:
                pass
            elif(BL<FL):
                BDifference=(BML-BL)-1;#include current one
                FML +=BDifference;
                BML = BL+1; #include current page

            elif(FL<BL and FL>=0):
                FDifference=(FML-FL);
                BML += FDifference;
                FML = FL+1;
                

            BSP=(pageNumber+1)-BML;#Backward starting point
            if(BSP<=0):
                BSP=1;
            count=1;
            while(BSP<=pageNumber and BSP>0 and count<=BML):
                paginationPages.append(BSP);
                BSP +=1;
                count +=1;
            FEP=pageNumber+FL;
            FSP = pageNumber+1;
            
            count=1;

            while(FSP<=FEP and FSP<=totalPagesInt and count<=FML):
                paginationPages.append(FSP);
                FSP +=1;
                count = count+1;
        offSet = pageNumber*constants.content_pagination_limit-constants.content_pagination_limit;    
        response = Content.getMyContent(request.user.id,constants.content_pagination_limit,
            offSet);
        response['paginationPages']=paginationPages;
        return render(request,'content/list.html',{'response':response,'currentPage':pageNumber})
    else:
        return redirect('/accounts/signin/?next=/content/mycontent/1');

def preview(request,contentId):
    if request.user.is_authenticated:
        response = Content.getContentInfo(contentId,request.user.id);
        return render(request,'content/preview.html',{'response':response});
    else:
        return redirect(('/accounts/signin/?next=/content/preview/{}').format(id));

@api_view(['POST'])
def delete(request):
    if(request.method == 'POST'):
        isWeb = False;
        accessToken = request.POST.get('accessToken');
        if(accessToken=="web"):
            if(request.user.is_authenticated):
                accessToken=request.user.id;
                isWeb=True;
            else:
                return JsonResponse({'statusCode':200,
            'status':'Invalid session'});

        result = Content.deleteMyContent(request.POST.get('c_id'),
            accessToken,isWeb);
        return JsonResponse(result);
    else:
        return JsonResponse({'statusCode':1,
            'status':'Invalid request'});

@api_view(["POST"])
def listMyContentAPI(request):
    if(request.user.is_authenticated):
        pageNumber = int(request.POST.get('pageNumber'));
        cType=request.POST.get('type');
        totalValues=Content.getTotalContent(request.user.id,cType);
        totalPages= totalValues/content_pagination_limit;
        totalPagesInt = int(totalPages);
        paginationPages=[];
        if(totalPagesInt<totalPages):
            totalPagesInt+=1;
        #Backward,ForwardLimits
        BML,FML,BL,FL=5,5,(pageNumber-1),(totalPagesInt-pageNumber);
        
        if(BL>0 or FL>0):    
            if BL>=5 and FL>=5:
                pass
            elif(BL<FL):
                BDifference=(BML-BL)-1;#include current one
                FML +=BDifference;
                BML = BL+1; #include current page

            elif(FL<BL and FL>=0):
                FDifference=(FML-FL);
                BML += FDifference;
                FML = FL+1;
                

            BSP=(pageNumber+1)-BML;#Backward starting point
            if(BSP<=0):
                BSP=1;
            count=1;
            while(BSP<=pageNumber and BSP>0 and count<=BML):
                paginationPages.append(BSP);
                BSP +=1;
                count +=1;
            FEP=pageNumber+FL;
            FSP = pageNumber+1;
            
            count=1;

            while(FSP<=FEP and FSP<=totalPagesInt and count<=FML):
                paginationPages.append(FSP);
                FSP +=1;
                count = count+1;
        offSet = pageNumber*constants.content_pagination_limit-constants.content_pagination_limit;    
        response = Content.getMyContent(request.user.id,constants.content_pagination_limit,
            offSet,cType);
        response['paginationPages']=paginationPages;
        response['currentPage'] = pageNumber;
        response['totalValues'] = totalValues;
        return JsonResponse(response);
        
    else:
        return JsonResponse({'statusCode':2,
            'status':'Invalid session, please login'});

@login_required
def listPendingApprovals(request):
    pass