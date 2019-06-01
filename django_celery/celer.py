# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from celery import Celery, platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

platforms.C_FORCE_ROOT = True   # 允许用root用户启动celery

app = Celery('django_celery')
app.config_from_object('django.conf:settings')
# 发现任务文件 -- app下task.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
