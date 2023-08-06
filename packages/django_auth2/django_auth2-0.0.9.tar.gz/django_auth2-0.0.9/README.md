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


celery
[first state with celery. django]: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html