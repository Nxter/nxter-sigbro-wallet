#!/bin/bash -x 

cd ../../../../../ansible/ 
vim deploy_sigbro_wallet.yml
ansible-playbook -Dv deploy_sigbro_wallet.yml --ask-vault-pass

