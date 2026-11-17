from django.urls import path
from .views import (
    task_list,
    task_create,
    task_stats,
    task_detail,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,

)

urlpatterns = [
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/stats/', task_stats, name='task_stats'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list_create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view() ,name='subtasks_detail'),
]
