#!/bin/sh

echo "======================================"
echo "  Django CI/CD Demo - Iniciando..."
echo "======================================"

# Esperar a que PostgreSQL esté disponible
echo "[1/3] Esperando a PostgreSQL en $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
  echo "  ... PostgreSQL no disponible aún, reintentando..."
done
echo "  PostgreSQL listo."

# Ejecutar migraciones
echo "[2/3] Ejecutando migraciones..."
python manage.py migrate --noinput

# Iniciar servidor con Gunicorn
echo "[3/3] Iniciando Gunicorn en 0.0.0.0:8000..."
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --log-level info
