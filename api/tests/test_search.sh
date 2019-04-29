#!/bin/bash

# bug 2018-03-24 for search multiaccount 
echo -e "\n---SEARCH MULTI ACCOUNT--------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/SMUN-JAHA-KGNR-9YG3R

exit

# bug 2018-03-23 for show multi_show_account SMUN-JAHA-KGNR-9YG3R when Nxt account does not exist
echo -e "\n---MULTI ACCOUNT--------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/account/SMUN-JAHA-KGNR-9YG3R

echo -e "\n---MULTI ACCOUNT UNKNOWN--------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/account/SMUN-9AHA-KGNR-7YG3R

exit

# aaaaa
echo -e "\n-RANDOM STRINGS----------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/kljasdflkjasdf

# nxt account RS
echo -e "\n--NXT ACCOUNT---------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/NXT-FRNZ-PDJF-2CQT-DQ4WQ
# ardor account RS
echo -e "\n--ARDOR ACCOUNT---------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/ARDOR-NYJW-6M4F-6LG2-76FR5
echo -e "\n---MULTI ACCOUNT--------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/NYJW-6M4F-6LG2-76FR5
# nxt transaction
echo -e "\n--NXT TX---------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/13882812479165007475
# asset id
echo -e "\n--NXT ASSET ID---------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/17582972238882915337
# nxt block
echo -e "\n--NXT BLOCK ID---------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/17001300560161976526
# fxt ardor transaction
echo -e "\n---ARDOR FXT TX--------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/15127891718952387100
# ardor block
echo -e "\n---ARDOR BLOCK ID--------------------------------------------------------------------------------"
curl http://localhost:8010/api/explorer/search/7523903623337979429
echo -e "\n-----------------------------------------------------------------------------------"


# nxt asset name
#curl http://localhost:8010/api/explorer/search/JLRDA
# nxt monetary name
#curl http://localhost:8010/api/explorer/search/SCORK


#curl http://localhost:8010/api/explorer/search/
#curl http://localhost:8010/api/explorer/search/
#curl http://localhost:8010/api/explorer/search/
#curl http://localhost:8010/api/explorer/search/
