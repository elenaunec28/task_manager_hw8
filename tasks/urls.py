from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import (
#     task_list,
#     task_create,
#     task_stats,
#     task_detail,
#     SubTaskListCreateView,
#     SubTaskDetailUpdateDeleteView,
#
# )
from .generic_views import (
    TaskListCreateView,
    task_stats,
    TaskRetrieveUpdateDestroyView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    MyTaskListView,
)

from .viewset_views import CategoryViewSet


# urlpatterns = [
#     path('tasks/', task_list, name='task_list'),
#     path('tasks/create/', task_create, name='task_create'),
#     path('tasks/stats/', task_stats, name='task_stats'),
#     path('tasks/<int:pk>/', task_detail, name='task_detail'),
#
#     path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list_create'),
#     path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view() ,name='subtasks_detail'),
# ]


router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task_list'),
    # path('tasks/create/', task_create, name='task_create'),
    path('tasks/stats/', task_stats, name='task_stats'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task_detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list_create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view() ,name='subtasks_detail'),

    path('', include(router.urls)),
    path('tasks/my/', MyTaskListView.as_view(), name='my-tasks'),
]

