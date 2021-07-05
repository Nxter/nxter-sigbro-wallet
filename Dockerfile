FROM scor2k/nginx:1.21.0

LABEL maintainer="scor2k <scor2k@gmail.com>"

ENV NGINX_PORT=8035
ENV NGINX_HOST=wallet.nxter.org

USER root

RUN rm -f /usr/share/nginx/html/* 
COPY . /usr/share/nginx/html/

USER nginx

EXPOSE 8035
