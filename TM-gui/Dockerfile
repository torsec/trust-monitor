### STAGE 1: Build ###
FROM node:latest AS build
WORKDIR /build

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm ci

COPY public/ public
COPY src/ src
RUN npm run build

### STAGE 2: Production Environment ###
FROM nginx:alpine
COPY --from=build /build/build/ /usr/share/nginx/html
#COPY ./.cert/tm-gui.crt /etc/nginx/certs/tm-gui.crt
#COPY ./.cert/tm-gui.key /etc/nginx/certs/tm-gui.key
#COPY ./.cert/extend_tls.conf /etc/nginx/conf.d/extend_tls.conf
#EXPOSE 443
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

## docker run -d -p 8080:80 tm-web-app:0.1 