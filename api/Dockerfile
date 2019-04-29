FROM python:3.6.3-jessie

LABEL maintainer "scor2k <scor2k@gmail.com>"

# let the container know that there is no tty
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/sigbro/database
WORKDIR /opt/sigbro

VOLUME /opt/sigbro/database

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY inc ./inc
COPY route ./route
COPY *.py ./

EXPOSE 8020

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8020 --timeout 120 --workers=1 --log-level=info"
CMD [ "gunicorn", "main:routes.app" ]
