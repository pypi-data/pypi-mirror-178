import os
from dotenv import load_dotenv
from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from .forms import SubscribeForm
from .models import Subscriber, EmailTemplate

load_dotenv()

class SubscribeView(View):
    template_name = "subscribe_form.html"
    form = SubscribeForm()
    context = {"form": form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    @method_decorator(csrf_protect)
    def post(self, request):
        try:
            if request.POST["subscribe_check"] == "on":
                subscriber = Subscriber(user=request.user, is_subscribed=True, subscribed_date=timezone.now())
                subscriber.save()
                subscriber.refresh_from_db()
        except KeyError:
            pass
        finally:
            return HttpResponseRedirect(reverse("email_app:subscribe"))


def send_email(request):
    subscribers = Subscriber.objects.all()
    sub_name_list = []
    sub_list = []
    for sub in subscribers:
        if sub.is_subscribed:
            sub_list.append(str(sub.user.email))
            sub_name_list.append(str(sub.user.username))

    email_template = EmailTemplate.objects.order_by("email_template_added").last()
    email_subject = str(email_template.subject_text)
    email_body = str(email_template.body_text)
    
    for name in sub_name_list:
        new_email_body = email_body.replace("[name]", name)

    for sub in sub_list:
        
        send_mail(
            email_subject,
            new_email_body,
            "blogpad@zohomail.com",
            [sub],
            fail_silently=False,
            auth_user="blogpad@zohomail.com",
            auth_password=os.environ["EMAIL_PASSWORD"],
        )

    return HttpResponse(new_email_body)
