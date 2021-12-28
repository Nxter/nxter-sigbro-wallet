# nxter-sigbro-wallet

Fast and simble wallet for Ardor Sigbro Project. It can generate QR code for Sigbro Mobile App [https://www.nxter.org/sigbro/] 

## Change log

### 3.25.2
  - fix: bugfix the corner cases with full collections

### 3.25.1
  - fix: remove faucet button

### 3.25.0
  - feat: transferAsset template type 

### 3.24.1
  - verify the public key

### 3.24.0
  - added button 'faucet'
  - added page 'activate' which show faucet instruction

### 3.23.1
  - fix the issue with the public key announcement for ardor transactions

### 3.23.0
  - make sigbro.js with hash

### 3.22.0
  - update url pattern for deeplinks

### 3.21.0
  - finally remove MPG
  - handle `Enter` button on the login page
  - replace Bitswift -> BITS
  - cache for the balance is 1 min instead of 5
  - added more info about NFT + icon
  - support @ for aliases
  - new docker image

### 3.20.1
  - remove MPG from operations

### 3.20.0
  - login with aliases

### 3.19.0
  - Show GPS balance
  - Remove MPG balance
  - Use local numbers format with max 2 digits instead of regexp
  - Updated icons
  - Updated footer links
  - Fixed bug with absent assets/currencies

### 3.18.0
  - Html reformat
  - Added new categories

### 3.17.0
  - Added upload form for the NFTv2 (IPFS version)

### 3.16.1
  - Added caption about upload size limit

### 3.16.0
  - Sigbro Auth was updated

### 3.15.0
  - Added required fiels
  - Disable collections that are already finished 

### 3.14.0
  - Added collection support

### 3.13.0
  - Tranfromed "upload a file to the Data Clound" into "Upload a NFTMagic file"

### 3.12.0
  - Add new section "Upload a file to the Data Cloud"

### 3.11.0
 - Can use ?page= and ?account= get params

### 3.10.1
 - Bugfix caching

### 3.10.0
 - Update Alerts GUI
 - Added cache for alerts

### 3.9.2
 - Removed warning msg

### 3.9.1
 - Added warning msg

### 3.9.0
 - Block outgoing transaction to the account without publicKey
 - Ask for recipientPublicKey if not exists
 - Replace random.nxter.org => random.api.nxter.org 

### 3.8.0
 - Added Max Property Group (MPG)

### 3.7.1
 - Rescued profile section
 - Updated balances view
 - Show alert for new accounts

### 3.7.0
 - Updated structure (merged portfolio and profile into balances)
 - Removed AEUR
 - Hid logo on the mobile view
 - Updated caption on the button which change network

### 3.6.1
 - Updated text on the SIGBRO mobile login form

### 3.6.0
 - Fixed GUI a little bit
 - Added 'OFFLINE' section for broadcast signed bytes to network

### 3.5.3
 - GUI fixes

### 3.5.2
 - removed checkbox 'encrypted msg' because we cannot garanty security of this operation
 - removed "show transaction" for template.
 - updated the text labels for the qr code 

### 3.5.1
 - fixed typo and added welcom message

### 3.5.0
 - added ALERTS section

### 3.4.0
 - removed NXT

### 3.3.3
 - update qr logos

### 3.3.2
 - disabled all childchains from leasing list except ardor

### 3.3.1
 - disabled cache for html pages

### 3.3.0
 - added sigbro logo to qr-codes. black for the testnet and red for the mainnet

### 3.2.0
 - leaseBalance operation

### 3.1.0
 - change between test/main network 

### 3.0.0
 - move to the new API
 - increase timeout for send money operation (GPRS not work)
 - fix operation links