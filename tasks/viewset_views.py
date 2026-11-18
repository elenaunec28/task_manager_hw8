from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category
from .serializers import CategoryCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories = Category.objects.annotate(task_count=Count('tasks'))
        data = [
            {
                'id': category.id,
                'name': category.name,
                'task_count': category.task_count,
            }
            for category in categories
        ]
        return Response(data)