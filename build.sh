#!/bin/bash

VER='3.9.1'

IMAGE_NAME='nxter-sigbro-wallet-web'

docker build --tag scor2k/$IMAGE_NAME:$VER .
docker push scor2k/$IMAGE_NAME:$VER
