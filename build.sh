#!/bin/bash

VER='3.29.0'

USER_NAME='scor2k'
IMAGE_NAME='nxter-sigbro-wallet-web'

MD5=`md5 js/sigbro.js | awk  '{ print $4 }'`

cp js/sigbro.js js/sigbro-$MD5.js
cp index.html index-backup.html

sed "s/sigbro.js/sigbro-$MD5.js/" index-backup.html > index.html

docker build --build-arg TARGETPLATFORM=linux/arm64 -f Dockerfile.arm64 -t $USER_NAME/$IMAGE_NAME:$VER-arm .
docker push $USER_NAME/$IMAGE_NAME:$VER-arm

rm -f js/sigbro-$MD5.js
mv index-backup.html index.html
