"""URL patterns para la app Tasks."""

from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('api/tasks/', views.api_tasks, name='api_tasks'),
    path('api/health/', views.api_health, name='api_health'),
]
