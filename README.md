# Django Celery Redis Flower

所需安装包及版本

django==1.11.6

celery==4.3.0

flower 0.9.2 (0.9.3在python2.7安装出错)

redis==3.2.1

基于django运行所需安装包

django-celery-results==1.1.1

django-celery-beat==1.5.0

------

遇到的小问题

django-admin startapp app_01

生成apps.py但是当把app都统一放入到apps文件夹下会找不到app，对apps产生冲突

django-admin startapp app_01 [directory]

------

项目初始化

django-admin startproject django_celery

django-admin startapp app_01 apps

修改项目

django_celery/django_celery/\_\_init\_\_.py

```python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .celery import app as celery_app

__all__ = ['celery_app']
```

django_celery/django_celery/celery.py

```python
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
```

django_celery/apps/app_01/task.py

```python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

```

视图函数

```python
from django.http import JsonResponse
from app01 import tasks
# Create your views here.
def index(request):
  res=tasks.add.delay(1,3)
  #任务逻辑
  return JsonResponse({'status':'successful','task_id':res.task_id})
```

flower

```
celery flower -A django_celery --address=127.0.0.1 --port=5555
```

django模式启动

配置settings.py，注册app

```python
INSTALLED_APPS = (
  ...,
  'django_celery_results',
)
```

修改backend配置，将redis改为django-db

```python
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = 'django-db' #使用django orm 作为结果存储
```

修改数据库

```python
python manage.py migrate django_celery_results
```

beat插件安装

```python
INSTALLED_APPS = [
  ....  
  'django_celery_beat',
]
```

修改数据库

```python
python manage.py migrate django_celery_beat
```

分别启动woker和beta

```celery
celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler #启动beta 调度器使用数据库
celery worker -A taskproj -l info #启动woker
```
