# -*- coding: utf-8 -*-

from datetime import timedelta
from celery.schedules import crontab

# 哨兵配置
# CELERY_BROKER_URL = "sentinel://localhost:26377/;sentinel://localhost:26378/;sentinel://localhost:26379/"
# CELERY_BROKER_TRANSPORT_OPTIONS = {"master_name": "mymaster"}
# # CELERY_RESULT_BACKEND = ""  # 不支持sentinel

BROKER_URL = 'redis://localhost:6379/0'  # Broker配置，使用Redis作为消息中间件
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 使用redis作为结果存储

CELERY_RESULT_BACKEND = 'django-db' #使用django orm 作为结果存储

CELERY_WORKER_MAX_TASKS_PER_CHILD = 100000  # 每个worker执行10w个任务就会被销毁，可防止内存泄露
CELERY_RESULT_EXPIRES = 3600 * 24  # 任务清除时间
CELERY_TASK_IGNORE_RESULT = True  # 一般不关注结果，请开启该设置，如果要存结果，请配置CELERY_RESULT_BACKEND
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_TASK_DEFAULT_EXCHANGE = 'celery_exchange'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_QUEUE = 'celery_queue'  # 默认是celery,一般修改
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

CELERY_BROKER_HEARTBEAT = 10  # 心跳
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案

# crontab任务
CELERY_BEAT_SCHEDULE = {
    'task_01': {
        'task': 'apps.app_01.tasks.add',
        'schedule': crontab(minute='0', hour='0'),  # 每日0点执行一次
    },
    'task_02': {
        'task': 'apps.app_01.tasks.mul',
        'schedule': timedelta(seconds=30),  # 每30秒执行一次
    },
}

# 分离2个任务队列
# from kombu import Exchange, Queue
# CELERY_QUEUES = (
#     Queue('default', Exchange('default'), routing_key='default'),
#     Queue('for_task_a', Exchange('for_task_a'), routing_key='for_task_a'),#这个是主动任务的队列
#     Queue('for_task_b', Exchange('for_task_b'), routing_key='for_task_b'),#这个是定时任务的队列
# )
# CELERY_ROUTES = {
#     'task_a': {'queue': 'for_task_a', 'routing_key': 'for_task_a'},
#     'task_b': {'queue': 'for_task_b', 'routing_key': 'for_task_b'},
# }

CELERY_SEND_TASK_ERROR_EMAILS = True  # 错误发送邮件
# 收件人
ADMINS = (
    ('xxxx', 'xxxx@xxxx.com'),
)
SERVER_EMAIL = 'xxx@xxx.com'
EMAIL_HOST = 'xxxx'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxxx@xx.com'
EMAIL_HOST_PASSWORD = '123456'
