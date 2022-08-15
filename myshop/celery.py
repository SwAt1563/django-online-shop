import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


'''
For asynchronous tasks 
it will search about tasks in the tasks file in each application

Note: don't forget to import celery in myshop/__init__.py file

'''