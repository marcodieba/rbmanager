#!/bin/bash
set -euo 
#pipefail

# Aguardar alguns segundos para garantir que o banco de dados esteja pronto
echo "Aguardando o banco de dados estar pronto..."
sleep 10

# Execute as migrações
echo "Executando migrações..."
# pipenv run python manage.py migrate --noinput

# Colete os arquivos estáticos
echo "Coletando arquivos estáticos..."
pipenv run python manage.py collectstatic --noinput

# Expande a variável de ambiente PORT e executa o Daphne
echo "Iniciando o servidor Daphne na porta ${PORT:-8000}..."
exec daphne -b 0.0.0.0 -p ${PORT:-8000} core.asgi:application
