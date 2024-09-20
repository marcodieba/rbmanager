#!/bin/bash
set -e

# Execute as migrações
pipenv run python manage.py migrate

# Colete os arquivos estáticos
pipenv run python manage.py collectstatic --noinput


# Expande a variável de ambiente PORT e executa o Daphne
exec daphne -b 0.0.0.0 -p ${PORT:-8000} core.asgi:application
