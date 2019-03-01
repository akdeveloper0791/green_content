from time import sleep
from models import GroupMemberAssignNotification

#list latest 100 pending email requests
pendingList = GroupMemberAssignNotification.objects.all().order_by(id)[:100];
for notification in pendingList.iterator():
    print(notification.members)

print("INside Send Group Assign notifications",flush=True);
sleep(300);#sleep for 5 mintes