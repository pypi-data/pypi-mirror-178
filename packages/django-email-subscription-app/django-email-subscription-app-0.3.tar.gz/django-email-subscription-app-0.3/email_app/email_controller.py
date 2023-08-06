import os
import django


#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "email_proj.settings")
django.setup()

from .models import Subscriber, EmailTemplate

class EmailController():
    def __init__(self):
        pass

    def get_subscribers(self):
        subscribers = Subscriber.objects.all()
        for sub in subscribers:
            print(sub)

    def get_latest_email_template(self):
        pass


email_ctl = EmailController()
email_ctl.get_subscribers()