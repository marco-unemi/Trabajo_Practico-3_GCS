# Django CI/CD Demo — Gestor de Tareas

Proyecto Django para la práctica de **Gestión de la Construcción y Despliegue Continuo** (GESCONSOF — UNEMI).

## Stack Tecnológico
- **Backend:** Django 4.2 + Python 3.10
- **Base de datos:** PostgreSQL (producción) / SQLite (CI/testing)
- **CI/CD:** GitHub Actions + Docker
- **Contenedorización:** Docker + Docker Compose

## Estructura del Proyecto
```
django-cicd-project/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── project/          # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/            # App funcional
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
└── templates/        # Templates HTML
```

## Ejecución Local
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Ejecutar Tests
```bash
python manage.py test -v 2
```
