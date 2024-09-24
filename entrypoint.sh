#!/bin/bash
set -euo 
#pipefail

# Verifique se a variável PORT está definida, caso contrário use 8080
PORT="${PORT:-8080}"

# Execute as migrações
python manage.py migrate

# Colete os arquivos estáticos
python manage.py collectstatic --noinput

# Expande a variável de ambiente PORT e executa o Daphne
exec daphne -b 0.0.0.0 -p "$PORT" core.asgi:application
