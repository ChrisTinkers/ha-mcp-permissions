FROM python:3.12-alpine
ARG BUILD_VERSION=1.0.0
ARG BUILD_ARCH=amd64
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py diagnose.py ./
CMD ["sh", "-c", "python -u /app/diagnose.py; exec python -u /app/server.py"]
