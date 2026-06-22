# deploy-notes.md — Simulación de Despliegue Continuo

**Proyecto:** Django CI/CD Demo — Gestor de Tareas  
**Asignatura:** Gestión de la Configuración de Software — UNEMI  
**Práctica N°3:** Sesión 3 — Simulación del Despliegue Continuo

---

## 1. Descripción del flujo automatizado

El pipeline de CI/CD definido en `.github/workflows/ci.yml` ejecuta tres etapas en secuencia:

```
[Push a main]
      │
      ▼
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Job: test  │────▶│   Job: build     │────▶│  Job: deploy-sim    │
│             │     │                  │     │                     │
│ · Instala   │     │ · docker build   │     │ · Descarga imagen   │
│   deps      │     │ · Guarda imagen  │     │ · docker load       │
│ · migrate   │     │   como artefacto │     │ · docker compose up │
│ · test -v 2 │     │   (.tar.gz)      │     │ · curl health check │
└─────────────┘     └──────────────────┘     └─────────────────────┘
```

---

## 2. Prerrequisitos para despliegue local

| Herramienta    | Versión mínima | Verificación              |
|----------------|----------------|---------------------------|
| Docker Desktop | 24.x           | `docker --version`        |
| Docker Compose | 2.x (plugin)   | `docker compose version`  |
| Git            | 2.x            | `git --version`           |

---

## 3. Pasos de despliegue — Entorno local (simulación)

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/django-cicd-project.git
cd django-cicd-project
```

### Paso 2 — Construir y levantar los contenedores

```bash
docker compose up --build
```

Esto ejecuta en orden:
1. Descarga la imagen `postgres:15-alpine` de Docker Hub
2. Construye la imagen `django-cicd:latest` desde el `Dockerfile`
3. Inicia el contenedor `django_cicd_db` (PostgreSQL)
4. Espera a que el healthcheck de PostgreSQL pase (`pg_isready`)
5. Inicia el contenedor `django_cicd_web` (Django + Gunicorn)
6. El `entrypoint.sh` ejecuta `python manage.py migrate` automáticamente
7. Gunicorn queda escuchando en el puerto 8000

### Paso 3 — Validar desde el navegador

Abrir en el navegador:

| URL                              | Descripción              |
|----------------------------------|--------------------------|
| `http://localhost:8000/`         | Lista de tareas          |
| `http://localhost:8000/api/health/` | Health check → `{"status": "ok"}` |
| `http://localhost:8000/api/tasks/`  | API JSON de tareas       |
| `http://localhost:8000/admin/`   | Panel de administración  |

### Paso 4 — Crear usuario admin (opcional)

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 4. Pasos de despliegue — Desde artefacto del pipeline (simulado)

Este es el flujo que ejecuta el job `deploy-sim` en GitHub Actions:

```bash
# 1. Descargar el artefacto desde GitHub Actions (Manual)
#    → Ir a: Actions → último workflow → Artifacts → django-cicd-image → Download

# 2. Cargar la imagen en Docker local
docker load < django-cicd-image.tar.gz

# 3. Verificar que la imagen existe
docker images | grep django-cicd

# 4. Levantar sin reconstruir (usa la imagen cargada)
docker compose up -d --no-build

# 5. Validar con curl
curl http://localhost:8000/api/health/
# Respuesta esperada: {"status": "ok", "service": "django-cicd"}
```

---

## 5. Comandos útiles de gestión

```bash
# Ver contenedores activos
docker compose ps

# Ver logs en tiempo real
docker compose logs -f web

# Detener contenedores (conserva datos)
docker compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker compose down -v

# Ejecutar tests dentro del contenedor
docker compose exec web python manage.py test -v 2
```

---

## 6. Simulación de push a DockerHub (no ejecutado)

En un entorno real con credenciales configuradas como Secrets en GitHub:

```bash
# Configurar en GitHub: Settings → Secrets → Actions
# DOCKERHUB_USERNAME = tu_usuario
# DOCKERHUB_TOKEN    = tu_token

docker tag django-cicd:latest TU_USUARIO/django-cicd:latest
docker push TU_USUARIO/django-cicd:latest
```

---

## 7. Estructura de artefactos generados

| Artefacto              | Generado en       | Descripción                        |
|------------------------|-------------------|------------------------------------|
| `django-cicd-image.tar.gz` | Job: build    | Imagen Docker comprimida           |
| Reporte de tests       | Job: test         | Visible en el log de GitHub Actions|
| Imagen en Docker local | Job: deploy-sim   | Cargada con `docker load`          |

---

*Documento generado para la Práctica N°3 — GESCONSOF — UNEMI*
