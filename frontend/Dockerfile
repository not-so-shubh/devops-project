FROM node:24-alpine@sha256:44fce696f38ba8c987c4db89954051000bbd05ffd8d8659ba15ed4a8602e937f AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

FROM nginxinc/nginx-unprivileged:stable-alpine@sha256:782bb89768cc87b7f95c18b95baa1af250e5d451f26794f59363540161147c01
# The pinned base contains libexpat 2.8.5-r0 (CVE-2026-77214).
# Require the fixed package from the same supported Alpine repository.
USER root
RUN apk add --no-cache 'libexpat>=2.9.0-r0'
COPY --chown=101:101 --from=build /app/dist /usr/share/nginx/html
# Retain dependency manifests outside the web root so Trivy also inventories JS packages.
COPY --chown=101:101 package.json package-lock.json /usr/share/stockpilot/
COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf
# The image supports an unprivileged Nginx on 8080. No runtime templating is needed.
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD ["wget", "-q", "--spider", "http://127.0.0.1:8080/healthz"]
ENTRYPOINT ["nginx", "-g", "daemon off;"]
