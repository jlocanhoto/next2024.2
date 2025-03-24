FROM node:22.14-bookworm AS dev

WORKDIR /app

COPY . .

RUN npm i

CMD ["npm", "run", "dev"]

FROM node:22.14-bookworm AS builder

ARG BACKEND_API_PUBLIC_URL
ENV VITE_API_URL=$BACKEND_API_PUBLIC_URL

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN NODE_ENV=production npm run build

FROM nginx:1.27.4-alpine AS prod

WORKDIR /usr/share/nginx/html

COPY --from=builder /app/dist ./

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
