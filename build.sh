#!/bin/bash

VER='3.0.0'

IMAGE_NAME='sigbro-wallet-web'

docker build --tag scor2k/$IMAGE_NAME:$VER .
docker push scor2k/$IMAGE_NAME:$VER
