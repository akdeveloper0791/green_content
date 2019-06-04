from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def contextualAdsRules(request):
    if request.user.is_authenticated:
        return render(request,'iot_device/contextual_ad_rules.html');
    else:
        return render(request,'iot_device/contextual_ad_rules.html');
