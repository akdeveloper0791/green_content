
from time import sleep
from django.core.mail import EmailMessage
from django.db import connection

# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#
## assuming your django settings file is at '/home/adskite/mysite/mysite/settings.py'
## and your manage.py is is at '/home/adskite/mysite/manage.py'
path = '/home/adskite/myproject/signagecms'
if path not in sys.path:
    sys.path.append(path)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'signagecms.settings'

#list latest 100 pending email requests
query = "SELECT * FROM group_groupmemberassignnotification LIMIT 100 order by id ASC";
with connection.cursor() as cursor:
    cursor.execute(query);
    values = cursor.fetchAll();
print(query);

'''pendingList = GroupMemberAssignNotification.objects.all().order_by(id)[:100];
for notification `in pendingList.iterator():
    print(notification.members)

print("INside Send Group Assign notifications",flush=True);
sleep(300);#sleep for 5 mintes'''