FROM caddy:builder AS builder
RUN xcaddy build \
    --with github.com/caddyserver/forwardproxy@caddy2=github.com/klzgrad/forwardproxy@naive

FROM caddy:latest
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
