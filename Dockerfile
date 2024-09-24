# Use a imagem base Debian
FROM python:3.9

# Definir argumentos e variáveis de ambiente
ARG DEBIAN_FRONTEND=noninteractive

ENV LANG=pt_BR.UTF-8 \
    LANGUAGE=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PORT=8000  
    # Railway definirá a porta correta no momento da execução

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
    python3 -m pip install --upgrade pip \
    python3 -m pip install pipenv && \

# Criação do usuário 'srv'
RUN useradd -m -d /srv srv

# Define o diretório de trabalho e atribui permissões
WORKDIR /srv
RUN chown -R srv:srv /srv

# Copia o arquivo requirements.txt e instala as dependências
COPY --chown=srv:srv requirements.txt /srv/
RUN pip install --no-cache-dir -r requirements.txt  # Instala dependências do requirements.txt

# Copia o script de entrada e garante que ele tenha permissão de execução
COPY --chown=srv:srv ./entrypoint.sh /srv/entrypoint.sh
RUN chmod +x /srv/entrypoint.sh

# Copia o código fonte da aplicação
COPY --chown=srv:srv ./src /srv

# Usa o Dumb-init como entrypoint
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/srv/entrypoint.sh"]

# CMD padrão, usa a variável de ambiente PORT definida pelo Railway
# CMD ["daphne", "-b", "0.0.0.0", "-p", "$PORT", "core.asgi:application"]
