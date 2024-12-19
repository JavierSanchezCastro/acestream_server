FROM ubuntu:22.04

ARG ACE_STREAM_VERSION

# Establecer la variable de entorno dentro del contenedor
ENV ACE_STREAM_VERSION=$ACE_STREAM_VERSION

# Instalación de dependencias
RUN apt-get update && apt-get install -y \
    wget \
    python3 \
    python3-pip \
    libpython3.10 \
    #coreutils \
    && rm -rf /var/lib/apt/lists/*

# Descargar y extraer AceStream, luego instalar dependencias de Python
RUN wget "https://download.acestream.media/linux/${ACE_STREAM_VERSION}.tar.gz" \
    && tar zxvf ${ACE_STREAM_VERSION}.tar.gz --one-top-level \
    && pip3 install --no-cache-dir -r /${ACE_STREAM_VERSION}/requirements.txt \
    && rm -rf ${ACE_STREAM_VERSION}.tar.gz

## Mover AceStream extraído a la carpeta /opt/acestream
#RUN mv {ACE_STREAM_VERSION} /opt/acestream

# Exponer el puerto de comunicación
EXPOSE 6878/tcp

# Definir el comando principal para ejecutar el contenedor
ENTRYPOINT /$ACE_STREAM_VERSION/start-engine --client-console
