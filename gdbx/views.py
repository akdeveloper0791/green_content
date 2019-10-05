from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from signagecms.constants import DROP_BOX_ACCESS_TOKEN;
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['POST'])
def getGDbxxx(request):
    if(request.method == "POST" and request.user.is_authenticated):       
        host = request.META['HTTP_HOST'];
        server = request.META['SERVER_NAME'];
        if((server=="www.signageserv.ai" and host=="www.signageserv.ai") or host=="192.168.0.143:8080" or host=="www.sunriosignage.com" or (server=="www.ihealthtv.com" and host=="www.ihealthtv.com")):
            return JsonResponse({'xxdd':DROP_BOX_ACCESS_TOKEN});
        else:
            return JsonResponse({});
    else:
        return JsonResponse({});