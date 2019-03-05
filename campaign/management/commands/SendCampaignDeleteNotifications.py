from django.core.management.base import BaseCommand
from campaign.models import Deleted_Campaigns
from django.template.loader import  get_template
from django.core import mail
from django.core.mail import EmailMessage

class Command(BaseCommand):
    help = "Send Campaign delete notifications"

    def handle(seld,*args,**kwargs):
        deletedCampaigns = Deleted_Campaigns.objects.all().order_by('id')[:100];
        print("Total deleted campaigns{} -".format(deletedCampaigns.count()));
        from_email = "contact@adskite.com"
        for campaign in deletedCampaigns.iterator():
          try:
            with mail.get_connection() as connection:
                ctx = {
                'campaign': campaign.campaign_name,
                'mac': campaign.mac,
                'deleted_at':campaign.deleted_at
                } 
                message = get_template('campaign/delete_campaign_notification.html').render({'info':ctx})
                to = [campaign.user.email];
                msg = EmailMessage("Green Content Campaign Delete Notification", message, to=to, from_email=from_email,
                        connection=connection)
                msg.content_subtype = 'html'
                response = msg.send();
                if(response==1):
                    campaign.delete();
                print("Delete campaign notification response-{}".format(response));
          except Exception as e:
            print("Error in sending delete campaign notifications - "+str(e),flush=True);

