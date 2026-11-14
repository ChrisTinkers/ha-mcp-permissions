FROM ghcr.io/home-assistant/base:3.24

RUN apk add --no-cache curl unzip ca-certificates && \
    curl -fsSL --retry 3 \
      -o /tmp/tunnel-client.zip \
      https://github.com/openai/tunnel-client/releases/download/v0.0.19/tunnel-client-runtime-v0.0.19-linux-amd64.zip && \
    echo 'a43beae6f08505a1b6751057d02797baa70a88ef7f9eb5dfd03a55b6b29116ad  /tmp/tunnel-client.zip' | sha256sum -c - && \
    mkdir -p /tmp/tunnel-extract && \
    unzip -q /tmp/tunnel-client.zip -d /tmp/tunnel-extract && \
    binary="$(find /tmp/tunnel-extract -type f -name tunnel-client-runtime | head -n 1)" && \
    test -n "$binary" && \
    cp "$binary" /usr/local/bin/tunnel-client-runtime && \
    chmod 755 /usr/local/bin/tunnel-client-runtime && \
    rm -rf /tmp/tunnel-client.zip /tmp/tunnel-extract

COPY run.sh /run.sh
RUN chmod 755 /run.sh

ARG BUILD_ARCH=amd64
ARG BUILD_VERSION=1.0.0
LABEL io.hass.type="app" \
      io.hass.arch="${BUILD_ARCH}" \
      io.hass.version="${BUILD_VERSION}"

CMD ["/run.sh"]
