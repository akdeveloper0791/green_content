from time import sleep

activate_this = "home/adskite/.virtualenvs/cms/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))


from cmsapp.models import User_unique_id,Multiple_campaign_upload

#from models import GroupMemberAssignNotification
#from sys.path import User_unique_id
#list latest 100 pending email requests
'''pendingList = GroupMemberAssignNotification.objects.all().order_by(id)[:100];
for notification in pendingList.iterator():
    print(notification.members)

print("INside Send Group Assign notifications",flush=True);
sleep(300);#sleep for 5 mintes'''
print (os.getcwd())