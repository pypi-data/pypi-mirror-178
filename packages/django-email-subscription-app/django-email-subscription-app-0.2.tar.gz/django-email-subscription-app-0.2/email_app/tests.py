from django.test import TestCase
from .models import Subscriber
from django.contrib.auth import get_user_model, authenticate, login
from django.utils import timezone
from django.urls import reverse

User = get_user_model()

def create_user_and_login():
    new_user = User.objects.create(username="test_username", password="test_password", email="test_email")
    new_user.save()
    user = authenticate(username="test_username", password="test_password")
    if user is not None:
        login(user=user)


class SubscriberModelTests(TestCase):

    def test_creates_subscriber(self):
        """  
        create subscriber return true if subscriber is created successfully
        """
        user = User.objects.create(username="test_username", password="test_password", email="test_email")

        subscribed_user = Subscriber(user=user, is_subscribed=True, subscribed_date=timezone.now())
        subscribed_user.save()
        subscribed_user.refresh_from_db()

        subscriber_data = Subscriber.objects.get(pk=1)
        
        self.assertEqual(subscriber_data.is_subscribed, True)



    def test_subscribe_view_get_template(self):
        """
        get subcribe view response, return true if repsonse code is 200
        """
        response = self.client.get(reverse("email_app:subscribe"))
        return self.assertEqual(response.status_code, 200)