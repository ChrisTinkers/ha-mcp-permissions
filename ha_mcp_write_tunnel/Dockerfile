FROM alpine:3.22
ARG BUILD_VERSION=1.0.0
ARG BUILD_ARCH=amd64
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
RUN apk add --no-cache ca-certificates jq
COPY --from=ghcr.io/openai/tunnel-client:v0.0.20 /usr/bin/tunnel-client /usr/local/bin/tunnel-client
COPY run.sh /run.sh
RUN chmod 0755 /run.sh
ENTRYPOINT ["/run.sh"]
