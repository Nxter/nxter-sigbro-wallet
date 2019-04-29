#!/bin/bash

echo -e "\n--URL 1---------------------------------------------------------------------------------"

curl -XPOST -H "Content-Type: application/json" http://localhost:8020/api/wallet/sendmoney -d '{"currencie":"nxt", "fee": -1, "amount" : 1, "recipient" : "NXT-FRNZ-PDJF-2CQT-DQ4WQ", "publicKey" : "e0914433305c721bbc5bb40f41ad3bc22304aac29d3c25ee8fb1bf40dde5ff3b" }'
