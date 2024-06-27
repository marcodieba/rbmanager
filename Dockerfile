# Use a imagem base Debian
FROM python:3.9

# Definir argumentos e variáveis de ambiente
ARG DEBIAN_FRONTEND=noninteractive

ENV LANG=pt_BR.UTF-8 \
    LANGUAGE=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    PYTHONUNBUFFERED=1

# Atualiza lista de pacotes e instala apt-transport-https
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-transport-https

# Instala pacotes necessários
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        locales \
        dumb-init \
        httpie \
        python3-pip \
        python3-setuptools \
        gettext \
        libpq-dev && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install pipenv && \
    echo "$LANG UTF-8" > /etc/locale.gen && \
    locale-gen

# Criação do usuário 'srv'
RUN useradd -m -d /srv srv

# Define o diretório de trabalho e atribui permissões
WORKDIR /srv
RUN chown -R srv:srv /srv

# Execute as migrações e cole os arquivos estáticos
#RUN python3 manage.py migrate
#RUN python3 manage.py collectstatic --noinput

# Expõe a porta 8000 (opcional, apenas para documentação)
EXPOSE 8000

# Usa o Dumb-init como entrypoint e inicia o Daphne
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# CMD padrão, pode ser substituído pelo docker-compose.yml
# CMD ["/usr/local/bin/daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

# Instala as dependências Python usando Pipenv
COPY --chown=srv Pipfile Pipfile.lock /srv/
RUN pipenv install --system --deploy --ignore-pipfile && \
    rm -f /srv/Pipfile*

RUN pipenv install psycopg
# Copia o código fonte da aplicação
COPY --chown=srv:srv ./src /srv

#RUN pipenv run python manage.py migrate
#RUN pipenv run python manage.py collectstatic --noinput

# Cria um arquivo de ambiente se necessário (opcional, pode ser definido no docker-compose.yml)
RUN touch /srv/core/.env
