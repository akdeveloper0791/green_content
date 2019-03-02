
from time import sleep
from django.core.mail import EmailMessage
from django.db import connection

print("INside Send Group Assign notifications",flush=True);

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

from models import GroupMemberAssignNotification

#list latest 100 pending email requests
query = "SELECT * FROM group_groupmemberassignnotification LIMIT 100";
with connection.cursor() as cursor:
    cursor.execute(query);
    values = cursor.fetchall();
print(query,flush=True);



#sleep(300);#sleep for 5 mintes'''