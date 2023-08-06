=====
Email Subscription App
=====

email subscription app is a Django emailing system for users to subscribe for emails and site admins to send prewritten, automated and personalized emails to thier application subscribers 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "email_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'email_app.apps.EmailAppConfig',
    ]

2. Include the email_app URLconf in your project urls.py like this::

    path("email_sub/", include("email_app.urls")),

3. Run ``python manage.py migrate`` to create the email_app models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a prewritten email template (you'll need the Admin app enabled).

5. send a post request to email_sub/subscribe/ to add the logged in user to subscriber database.

6. send a get request to http://127.0.0.1:8000/email_sub/send_mail/ to send your prewritten emails to all subscribers.
