# Use a imagem base Debian
FROM python:3.9

# Definir argumentos e variáveis de ambiente
ARG DEBIAN_FRONTEND=noninteractive

ENV LANG=pt_BR.UTF-8 \
    LANGUAGE=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    PYTHONUNBUFFERED=1

# Atualiza lista de pacotes e instala pacotes necessários
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        redis-tools \
        dumb-init \
        python3-pip \
        python3-setuptools \
        libpq-dev && \
    python3 -m pip install --upgrade pip && \
    pip install pipenv

# Criação do usuário 'srv'
RUN useradd -m -d /srv srv

# Define o diretório de trabalho e atribui permissões
WORKDIR /srv
RUN chown -R srv:srv /srv

# Copia o Pipfile e Pipfile.lock e instala as dependências
COPY --chown=srv:srv Pipfile Pipfile.lock /srv/
RUN pipenv install --system --deploy --ignore-pipfile

# Copia o código fonte da aplicação
COPY --chown=srv:srv ./src /srv

# Copia o script de entrada
COPY --chown=srv:srv ./entrypoint.sh /srv/entrypoint.sh
RUN chmod +x /srv/entrypoint.sh

# Usa o Dumb-init como entrypoint
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/bin/bash", "/srv/entrypoint.sh"]
