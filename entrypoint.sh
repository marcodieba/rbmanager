#!/bin/bash
set -euo 
#pipefail

# Execute as migrações
echo "Rodando migrações..."
python manage.py migrate --noinput

# Colete os arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Inicie o Daphne
echo "Iniciando Daphne no endereço 0.0.0.0:${PORT:-8000}..."
exec daphne -b 0.0.0.0 -p ${PORT:-8000} core.asgi:application
