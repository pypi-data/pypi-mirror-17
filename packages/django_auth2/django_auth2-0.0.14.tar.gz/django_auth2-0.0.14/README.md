#Django AUTH

###installing
    pip install django_auth2

in your project.settings

    INSTALLED_APPS = [
        ...
        'django.contrib.auth',
        'django_auth2',
    ]

in your project.urls

    ...
    url(r'', include('django_auth2.urls')),
    ...

in User model

    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField()


if want send activation email for activate user
then set DJANGO_AUTH2_SEND_ACTIVATION_EMAIL in yor project.settings user.is_active = False
else user.is_active = True (by default) and mail not sent

For send mail (example):

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'my_mail@gmail.com'
    EMAIL_HOST_PASSWORD = 'my_pass'
    EMAIL_PORT = 587

password reset days in project.settings

    PASSWORD_RESET_TIMEOUT_DAYS = 1

Your need create view with name "index" for redirect (after authentication)


you can use celery for send mails
if you virtualenv installed celery and project work with her;
  mails be sent from celery
else if installed celery but not project now work with her;
  mails message is not sent
[first state with celery. django]: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

if not celery then mail sent (default django)
