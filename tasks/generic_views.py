from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters
from rest_framework.decorators import api_view, action, permission_classes
# from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from .pagination import SubTaskPagination
from .permissions import IsOwnerOrReadOnly

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
    permission_classes = [IsAuthenticated]

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Task.objects.all()

        day = self.request.query_params.get('day')
        if day:
            queryset = queryset.filter(deadline__iso_week_day=int(day))

        return queryset


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskCreateSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
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
    permission_classes = [IsAuthenticated]
    pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'deadline': ['exact', 'gte', 'lte'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')

        task_title = self.request.query_params.get('task_title')
        status_param = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class MyTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)