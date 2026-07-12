# ==============================================================================
# Estágio Único: Imagem leve baseada em Debian para compatibilidade com Netcat OpenBSD
# ==============================================================================
FROM debian:12-slim

label maintainer="seu nome Gilmar Santana"
LABEL project="bash-commerce"

# Evita diálogos interativos durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Instalação do netcat-openbsd e limpeza de cache para otimização de camadas
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia o script com o nome original e o renomeia internamente no container para 'app.sh'
# Isso isola a complexidade do nome do arquivo da configuração do ENTRYPOINT
COPY sistema_e_commerce_web_bash.sh ./app.sh

# Garante permissão de execução para o script
RUN chmod +x ./app.sh

EXPOSE 80

ENTRYPOINT ["./app.sh"]
