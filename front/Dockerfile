FROM node:alpine as build

RUN npm install
COPY . . /messenger/front
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /dist /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/nginx.conf.d/default.conf
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]