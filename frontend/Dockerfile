# syntax=docker/dockerfile:1.7
FROM node:22.23.4-bookworm-slim AS builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=secret,id=npm_ca,target=/run/npm-ca.pem,required=false \
    if [ -f /run/npm-ca.pem ]; then \
      NODE_EXTRA_CA_CERTS=/run/npm-ca.pem npm ci; \
    else \
      npm ci; \
    fi

COPY frontend/ .

ARG VITE_API_BASE_URL=http://localhost:8000/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

FROM nginx:1.29.3-alpine

COPY --from=builder /app/frontend/dist /usr/share/nginx/html
COPY openapi.yaml /usr/share/nginx/html/openapi.yaml
COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
