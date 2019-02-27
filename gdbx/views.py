from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
def getGDbxxx(request):
    if(request.user.is_authenticated):
        #full_path = ('http', ('', 's')[request.is_secure], '://', request.META[0], );
        #full_path = ''.join(full_path);
        host = request.META['HTTP_HOST'];
        #return JsonResponse({'status':'true','full_path':full_path});
        return JsonResponse({'full_path':(host)});
    else:
        return JsonResponse({'status':'false'});