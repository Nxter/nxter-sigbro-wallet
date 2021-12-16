#!/bin/bash

VER='3.25.0'

IMAGE_NAME='nxter-sigbro-wallet-web'

MD5=`md5 js/sigbro.js | awk  '{ print $4 }'`

cp js/sigbro.js js/sigbro-$MD5.js
cp index.html index-backup.html

sed "s/sigbro.js/sigbro-$MD5.js/" index-backup.html > index.html

docker build --tag scor2k/$IMAGE_NAME:$VER .
docker push scor2k/$IMAGE_NAME:$VER

rm -f js/sigbro-$MD5.js
mv index-backup.html index.html

