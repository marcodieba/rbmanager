#!/bin/bash
set -e

# Execute as migrações
pipenv run python manage.py migrate

# Colete os arquivos estáticos
pipenv run python manage.py collectstatic --noinput

# Execute o comando passado como argumento (ou padrão do Dockerfile)
exec "$@"
