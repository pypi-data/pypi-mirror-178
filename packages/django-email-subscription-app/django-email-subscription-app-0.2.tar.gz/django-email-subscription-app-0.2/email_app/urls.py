from django.urls import path
from .views import SubscribeView
from . import views
app_name = "email_app"
urlpatterns = [
    path("send_mail/", views.send_email, name="send_mail"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
]
