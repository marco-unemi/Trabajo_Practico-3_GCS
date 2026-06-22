"""Tests para la aplicación Tasks."""

from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskModelTest(TestCase):
    """Tests para el modelo Task."""

    def setUp(self):
        """Crear una tarea de prueba."""
        self.task = Task.objects.create(
            title='Tarea de prueba',
            description='Descripción de prueba',
            priority='high',
        )

    def test_task_creation(self):
        """Verificar que la tarea se crea correctamente."""
        self.assertEqual(self.task.title, 'Tarea de prueba')
        self.assertEqual(self.task.priority, 'high')
        self.assertFalse(self.task.completed)

    def test_task_str(self):
        """Verificar la representación en string del modelo."""
        self.assertEqual(str(self.task), 'Tarea de prueba')

    def test_task_default_priority(self):
        """Verificar que la prioridad por defecto es 'medium'."""
        task = Task.objects.create(title='Tarea sin prioridad')
        self.assertEqual(task.priority, 'medium')

    def test_task_ordering(self):
        """Verificar que las tareas se ordenan por fecha descendente."""
        task2 = Task.objects.create(title='Segunda tarea')
        tasks = list(Task.objects.all())
        self.assertEqual(tasks[0], task2)  # La más reciente primero


class TaskViewTest(TestCase):
    """Tests para las vistas de Tasks."""

    def setUp(self):
        """Configurar el cliente y datos de prueba."""
        self.client = Client()
        self.task = Task.objects.create(
            title='Tarea vista',
            description='Para probar vistas',
        )

    def test_task_list_view(self):
        """Verificar que la lista de tareas responde con 200."""
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view(self):
        """Verificar que el detalle de tarea responde con 200."""
        response = self.client.get(
            reverse('tasks:task_detail', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_task_detail_404(self):
        """Verificar que una tarea inexistente retorna 404."""
        response = self.client.get(reverse('tasks:task_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class TaskAPITest(TestCase):
    """Tests para los endpoints API."""

    def setUp(self):
        """Configurar el cliente y datos de prueba."""
        self.client = Client()
        Task.objects.create(title='API Task 1', priority='low')
        Task.objects.create(title='API Task 2', priority='high')

    def test_api_tasks_endpoint(self):
        """Verificar que el endpoint de tareas retorna JSON."""
        response = self.client.get(reverse('tasks:api_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_api_tasks_count(self):
        """Verificar que retorna la cantidad correcta de tareas."""
        response = self.client.get(reverse('tasks:api_tasks'))
        import json
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_api_health_endpoint(self):
        """Verificar que el health check responde correctamente."""
        response = self.client.get(reverse('tasks:api_health'))
        self.assertEqual(response.status_code, 200)
        import json
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'ok')
