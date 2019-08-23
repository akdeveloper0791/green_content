from django.core.management.base import BaseCommand

import datetime
from license.models import License_Device
import pytz
from django.db.models import Q

class Command(BaseCommand):
    help = 'Sends Group assign notifications'

    def handle(self, *args, **kwargs):
        today = datetime.date.today();
        
        todayDateString = "{} {}".format(today.strftime("%Y-%m-%d"),
            "23:59:59")
        expiredDate = datetime.datetime.strptime(todayDateString,"%Y-%m-%d %H:%M:%S")
        expiredDate = expiredDate.astimezone(pytz.UTC);
        
        #get all expired devices
        expiredDevices = License_Device.objects.filter(Q(expiry_date__lte=expiredDate),Q(status=1) | Q(status=0)).update(status=-1);
        print(todayDateString+" updated :"+str(expiredDevices));