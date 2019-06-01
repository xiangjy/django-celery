# -*- coding: utf-8 -*-

from django.http import JsonResponse

from django_celery_beat.models import PeriodicTask  # 倒入插件model
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.viewsets import ModelViewSet

from apps.app_01 import tasks


def index(request):
    res = tasks.add.delay(1, 3)
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class MyPagination(pagination.PageNumberPagination):
    """自定义分页"""
    page_size = 2
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 4


class TaskView(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    pagination_class = MyPagination
