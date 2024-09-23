#!/bin/bash
set -euo 
#pipefail

# Defina PYTHONPATH
export PYTHONPATH=/srv

# Debug: Listar pacotes instalados
pip list

# Execute as migrações
python manage.py migrate

# Colete os arquivos estáticos
python manage.py collectstatic --noinput

# Expande a variável de ambiente PORT e executa o Daphne
exec daphne -b 0.0.0.0 -p "${PORT:-8080}" core.asgi:application
