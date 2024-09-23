#!/bin/bash
set -e

# # Execute as migrações
# pipenv run python manage.py migrate

# Colete os arquivos estáticos
pipenv run python srv/manage.py collectstatic --noinput

# # Execute o comando passado como argumento (ou padrão do Dockerfile)
# exec "$@"

# Expande a variável de ambiente PORT e executa o Daphne
exec daphne -b 0.0.0.0 -p ${PORT:-8080} core.asgi:application
