from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from accounts.models import ForgotPwdSession
class Command(BaseCommand):
    help = 'Sends Group assign notifications'

    def handle(self, *args, **kwargs):
        print(datetime.now(),flush=True);
        one_hour_from_now = datetime.now() + timedelta(hours=-1)
        print(one_hour_from_now,flush=True);
        invalidSessions = ForgotPwdSession.objects.filter(created_at__lte=one_hour_from_now);
        if invalidSessions.exists():
            for session in invalidSessions.iterator():
                session.delete();
        else:
            print("No sessions found");

