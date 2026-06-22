"""Vistas de la aplicación Tasks."""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task


def task_list(request):
    """Lista todas las tareas."""
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    """Detalle de una tarea específica."""
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def api_tasks(request):
    """API endpoint que retorna las tareas en JSON."""
    tasks = Task.objects.all().values(
        'id', 'title', 'description', 'completed', 'priority', 'created_at'
    )
    return JsonResponse(list(tasks), safe=False)


def api_health(request):
    """Health check endpoint para validar que el servicio está activo."""
    return JsonResponse({'status': 'ok', 'service': 'django-cicd'})
