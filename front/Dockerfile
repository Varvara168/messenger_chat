# Build stage
FROM node:alpine AS build

WORKDIR /messenger/front

# Сначала копируем package.json, чтобы кешировать npm install
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine

COPY --from=build /messenger/front/dist /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
