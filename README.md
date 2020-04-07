# nxter-sigbro-wallet

Fast and simble wallet for Ardor Sigbro Project. It can generate QR code for Sigbro Mobile App [https://www.nxter.org/sigbro/] 

## Change log

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