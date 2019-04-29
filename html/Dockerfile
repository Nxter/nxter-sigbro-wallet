FROM nginx:1.14.0-alpine

LABEL maintainer "scor2k <scor2k@gmail.com>"

RUN rm -f /usr/share/nginx/html/* 

COPY . /usr/share/nginx/html/

EXPOSE 80
