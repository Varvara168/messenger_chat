FROM nginx:stable-alpine
COPY package.json /usr/share/nginx/html/package.json
RUN npm install

COPY . .
RUN npm run build
FROM nginx:stable-alpine
COPY --from=build /disk /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
