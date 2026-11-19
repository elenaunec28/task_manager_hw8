from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['exact', 'gte', 'lte'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskCreateSerializer


@api_view(['GET'])
def task_stats(request):
    total = Task.objects.count()

    by_status_qs = Task.objects.values('status').annotate(count=Count('id'))
    by_status = {item['status']: item['count'] for item in by_status_qs}

    overdue = Task.objects.filter(deadline__lt=timezone.now()).exclude(status='Done').count()

    return Response({
        'total_tasks': total,
        'tasks_by_status': by_status,
        'overdue_tasks': overdue,
    })


# class SubTaskPagination(PageNumberPagination):
#     page_size = 5


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    # pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['exact', 'gte', 'lte'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer