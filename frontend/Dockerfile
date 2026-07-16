FROM node:22-alpine AS builder
WORKDIR /frontend
COPY package.json package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build

FROM nginxinc/nginx-unprivileged:1.29-alpine AS runner
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx --from=builder /frontend/dist /usr/share/nginx/html
EXPOSE 8080
