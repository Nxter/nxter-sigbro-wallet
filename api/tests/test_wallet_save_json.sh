#!/bin/bash

echo -e "\n--URL 1---------------------------------------------------------------------------------"
curl -X POST -d '{"senderPublicKey": "cbe8ebb42c46652270971aa550b925af282b0ba21147a732f276d14b4dc3be3f", "chain": 3, "feeNQT": "10", "type": 0, "version": 1, "fxtTransaction": "0", "phased": false, "ecBlockId": "14729870887677524122", "attachment": {"version.Message": 1, "messageIsText": true, "message": "9647d25bef9aa6a518d1", "version.OrdinaryPayment": 0}, "senderRS": "ARDOR-ZZZZ-48G3-9F9W-4CLJZ", "subtype": 0, "amountNQT": "65500", "sender": "3441394504758722559", "recipientRS": "ARDOR-ZZZZ-48G3-9F9W-4CLJZ", "recipient": "3441394504758722559", "ecBlockHeight": 205282, "deadline": 1440, "timestamp": 12203117, "height": 2147483647}'  http://localhost:8020/api/wallet/savejson


