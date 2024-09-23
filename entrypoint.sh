#!/bin/bash
set -e

# Ativa o ambiente virtual do Pipenv
# export PIPENV_VENV_IN_PROJECT=1
# pipenv install --deploy --ignore-pipfile

# # Execute as migrações
# pipenv run python manage.py migrate

# # Colete os arquivos estáticos
# pipenv run python manage.py collectstatic --noinput

# if [ "$RUN_COLLECTSTATIC" = "true" ]; then
#     python manage.py collectstatic --noinput
# fi


# Expande a variável de ambiente PORT e executa o Daphne
exec pipenv run daphne -b 0.0.0.0 -p ${PORT:-8080} core.asgi:application
