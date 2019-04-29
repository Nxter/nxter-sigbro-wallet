## SIGBRO WALLET API

### API ASSET

### API ARDOR WALLET
* /api/wallet/assets/{account}
* /api/wallet/currencies/{account}
* /api/wallet/savejson (POST)
* /api/wallet/json/{url} 

### Changelog
*2.2.4* 
* replace text for url with url

*2.2.3*
* add button for sigbro mobile app when qr is generated
* replace full URL to caption

*2.2.2*
* bugfix android old browser 

*2.2.1*
* bugfix function name in js
* clear sigbro_uuid when logout

*2.2.0*
* add SSE suppert 
* auth via sigbro mobile

*2.1.3*
* save uuid into locastorage with timestamp
* use old uuid if delta time less than 15 min
* send every new uuid to /api/auth/new

*2.1.2*
* add javascript sse for qr code (test)

*2.1.1*
* Show QR with uuid for login via SIGBRO MOBILE

*2.1.0*
* QR on login form for auth with sigbro

*2.0.5*
* fixed bug with untranslated words in assets and currencies
* add `encrypt_msg` button in web
* generate other json for encrypted msg

*2.0.2*
* new environment for use testnet

*2.0.1*
* Change local database to remote api `https://random.nxter.org/api/v3/save_tx`
* add test for save 

*2.0.0*
* Move to Single Page Application style for cordova
* add favicon
* add new keys from localstorage to clean

*1.1.1*
* add `send_post` to ardor. 
* modify `send_money` for ardor
* fix bug with adding new db record ( `get_or_none` vs `get` )
* fix bug with static chain number

*1.1.0*
* First public version

*1.0.4*
* new API for generate sendmoney transacti new API for generate sendmoney transaction `/api/wallet/sendmoney`

*1.0.3*
* new API for save and get json (needs for qr codes)

*1.0.2*
* new API for wallet: `api/wallet/currencies/{account}`
* new API for Nxt, Ardor: `get_currencies`

*1.0.1*
* Fix bug with unique id (name -> asset)
* Remove languages from new API
* Fix bug with wrong logo for ignis's assets

*1.0.0*
* new API for wallet: `/api/wallet/assets/{account}`
* new API for Ardor: `get_assets`
* new API for Nxt: `get_assets`
* initial release

