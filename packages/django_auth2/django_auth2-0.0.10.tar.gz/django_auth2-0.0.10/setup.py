import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django_auth2',
    version='0.0.10',
    description='Login, Registration, Reset password, ActivateUser',
    long_description=README,
    author='nick1994209',
    author_email='nick1994209@gmail.com',
    url='https://github.com/Nick1994209/django-auth2/',
    license='MIT',
    packages=find_packages(),
    # packages=['django_auth2'],
    include_package_data=True,
    install_requires=[
        'django',
        # 'celery' if your need
    ]
)
