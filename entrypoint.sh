#!/bin/sh

# Si falla cualquier comando, el script se detiene
set -e

echo "Esperando a que la base de datos esté lista..."

# Intentamos conectar a Postgres usando netcat (nc)
# El host 'db' y el puerto '5432' vienen de tu docker-compose
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Base de datos detectada. Aplicando migraciones..."
python manage.py migrate

echo "Iniciando servidor..."
exec "$@"