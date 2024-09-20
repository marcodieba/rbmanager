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
        redis-tools \
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

# Instala as dependências Python usando Pipenv
COPY --chown=srv Pipfile Pipfile.lock /srv/
RUN pipenv install --system --deploy --ignore-pipfile && \
    rm -f /srv/Pipfile*

RUN pip install gunicorn
RUN pipenv install psycopg
RUN pip install daphne

# Copia o script de entrada
COPY --chown=srv:srv entrypoint.sh /srv/entrypoint.sh
RUN chmod +x /srv/entrypoint.sh

# Usa o Dumb-init como entrypoint e inicia o Daphne com o script
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/srv/entrypoint.sh"]

# Copia o código fonte da aplicação
COPY --chown=srv:srv ./src /srv
