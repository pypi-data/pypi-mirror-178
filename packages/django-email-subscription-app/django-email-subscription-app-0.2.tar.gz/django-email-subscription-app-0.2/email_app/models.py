from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField()
    subscribed_date = models.DateTimeField()
    

class EmailTemplate(models.Model):
    subject_text = models.CharField(max_length=50)
    body_text = models.TextField()
    email_template_added = models.DateTimeField("Date Added")
        