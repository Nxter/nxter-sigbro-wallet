#!/bin/bash

VER=`cat __init__.py | grep __version__ | awk -F '=' '{print $2}' | sed 's/ //g' | sed 's/"//g'`

IMAGE_NAME='nxter-bridge-wallet-api'

docker build --tag scor2k/$IMAGE_NAME:$VER .
docker push scor2k/$IMAGE_NAME:$VER
