from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from signagecms.constants import DROP_BOX_ACCESS_TOKEN;
# Create your views here.
def getGDbxxx(request):
    if(request.method == "POST" and request.user.is_authenticated):       
        host = request.META['HTTP_HOST'];
        server = request.META['SERVER_NAME'];
        if((server=="www.greencontent.in" and host=="www.greencontent.in") or server=="DESKTOP-HARKF96" or (server=="www.signageserv.ai" and host=="www.signageserv.ai")):
            return JsonResponse({'xxdd':DROP_BOX_ACCESS_TOKEN});
        else:
            return JsonResponse({'host':server,'host':host});
    else:
        return JsonResponse({});