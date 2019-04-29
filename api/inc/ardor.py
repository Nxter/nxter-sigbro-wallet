# -*- coding: UTF-8 -*-

# Interface for wordpress explorer

# Global modules
import json
import datetime
import math
import time
import datetime
import requests
import re
import os

# Modules
from inc import utils

# Constants
DEFAULT_NODE_ADDRESS  = os.environ.get('DEFAULT_NODE_ADDRESS', 'random.nxter.org')
DEFAULT_NODE_PROTO    = os.environ.get('DEFAULT_NODE_PROTO', 'https')
DEFAULT_NODE_NETWORK  = os.environ.get('DEFAULT_NODE_NETWORK', 'main')

if DEFAULT_NODE_NETWORK == 'main' :
  NXT_PREFIX="nxt"
  ARDOR_PREFIX="ardor"
else:
  NXT_PREFIX="tstnxt"
  ARDOR_PREFIX="tstardor"


class Ardor():
  """ API for Explorer """

  def __init__(self):
    """ initialization """

  def __del__(self):
    """ destroing """

  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################

  def get_json(self, url):
    """GET request and return JSON response"""
    try:
      r = requests.get(url=url, timeout=3)
    except requests.exceptions.RequestException as e:
      tmp = """{"error" : "Connection timeout: %s " }""" % (url)
      data = json.loads(tmp)
      return data

    if r.status_code == 200:
      data = json.loads(r.text)
      return data
    else:
      tmp = """{"error" : "Error while try to get information from %s " }""" % (url)
      data = json.loads(tmp)
      return data

  ###############################################################################################################################################################################################
  def post_json(self, url, payload) :
    """Send POST request and return response"""

    try :
      r = requests.post( url=url, data=payload, timeout=3)
    except Exception as e :
      tmp = """{"error" : "%s" }""" % (e)
      data = json.loads(tmp)
      return data

    if r.status_code == 200 :
      return json.loads(r.text)
    else:
      tmp = """{"error" : "Error while try to get information from %s " }""" % (url)
      return json.loads(tmp)


  ###############################################################################################################################################################################################

  def get_account_exist(self, account):
    """ Check if account exist """
    # try to get account info
    # change 4 times getBalance to one getBalances
    url = """%s://%s/%s?requestType=getAccount&account=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )
    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)

    result = {
      "data"  : account,
      "error" : None
    }

    return json.dumps(result)

  ###############################################################################################################################################################################################

  def get_account_info_20180227(self, account):
    """ Get balance info form ARDR, IGNIS, AUEU, BITSWIFT """
    # try to get account info
    # change 4 times getBalance to one getBalances
    url = """%s://%s/%s?requestType=getAccount&account=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )
    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)

    if 'name' in res:
      name = res['name']
    else :
      name = ''


    if 'description' in res:
      description = res['description']
    else :
      description = ''

    # try to get ARDR balance
    url = """%s://%s/%s?requestType=getBalances&account=%s&chain=1&chain=2&chain=3&chain=4""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)

    if 'balances' in res :
      balances = res['balances']
    else :
      tmp = "{{Some problem when getting ARDR info}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }
      return json.dumps(result)
 
    ardrNQT     = balances["1"]['balanceNQT']
    ignisNQT    = balances["2"]['balanceNQT']
    aeurNQT     = balances["3"]['balanceNQT']
    bitswiftNQT = balances["4"]['balanceNQT']

    #### return data into show function
    result = {
      'accountRS'   : account, 
      'name'        : name,
      'description' : description,
      'ardorNQT'    : ardrNQT,
      'ignisNQT'    : ignisNQT,
      'aeurNQT'     : aeurNQT,
      'bitswiftNQT' : bitswiftNQT
    }

    return json.dumps(result)


  ###############################################################################################################################################################################################

  def get_account_info(self, account):
    """ Get balance info form ARDR, IGNIS, AUEU, BITSWIFT """
    # try to get account info
    url = """%s://%s/%s?requestType=getAccount&account=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )
    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)

    if 'name' in res:
      name = res['name']
    else :
      name = ''


    if 'description' in res:
      description = res['description']
    else :
      description = ''

    # try to get ARDR balance
    url = """%s://%s/%s?requestType=getBalance&account=%s&chain=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account, "ARDR" )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'balanceNQT' in res:
      ''' get ARDOR, going next '''
      ardrNQT = res['balanceNQT']
    else:
      tmp = "{{Some problem when getting ARDR info}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }
      return json.dumps(result)

    # try to get IGNIS balance
    url = """%s://%s/%s?requestType=getBalance&account=%s&chain=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account, "IGNIS" )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'balanceNQT' in res:
      ''' get IGNIS, going next '''
      ignisNQT = res['balanceNQT']
    else:
      tmp = "{{Some problem when getting IGNIS info}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }
      return json.dumps(result)

   # try to get AEUR balance
    url = """%s://%s/%s?requestType=getBalance&account=%s&chain=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account, "AEUR" )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'balanceNQT' in res:
      ''' get ARDOR, going next '''
      aeurNQT = res['balanceNQT']
    else:
      tmp = "{{Some problem when getting AEUR info}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }
      return json.dumps(result)

   # try to get BITSWIFT balance
    url = """%s://%s/%s?requestType=getBalance&account=%s&chain=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account, "BITSWIFT" )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'balanceNQT' in res:
      bitswiftNQT = res['balanceNQT']
    else:
      tmp = "{{Some problem when getting BITSWIFT info}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }
      return json.dumps(result)


    #### return data into show function
    result = {
      'accountRS'   : account, 
      'name'        : name,
      'description' : description,
      'ardorNQT'    : ardrNQT,
      'ignisNQT'    : ignisNQT,
      'aeurNQT'     : aeurNQT,
      'bitswiftNQT' : bitswiftNQT
    }

    return json.dumps(result)


  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################

  def get_fxt_info(self, fxt):
    # try to get public key for the sender
    url = """%s://%s/%s?requestType=getFxtTransaction&transaction=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, fxt )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'senderRS' in res:
      # looks like transaction exits!

      result  = {
        "data" : res
      }

    else:
      tmp = "{{We are sorry. Something goes wrong :(}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }

    return json.dumps(result)

  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################

  def get_hash_info(self, fullhash, chain):
    # try to get public key for the sender
    url = """%s://%s/%s?requestType=getTransaction&fullHash=%s&chain=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, fullhash, chain )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'senderRS' in res:
      # looks like transaction exits!

      result  = {
        "data" : res
      }

    else:
      tmp = "{{We are sorry. Something goes wrong :(}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }

    return json.dumps(result)



  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################

  def get_public_key(self, sender, lang='en'):
    """ Get Public Key"""

    pubKey = ''

    # try to get public key for the sender
    url = """%s://%s/%s?requestType=getAccountPublicKey&account=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, sender )
    print (url)

    res = self.get_json(url)

    #tmp = """{"error" : None, "data" : None  }""" 

    if 'error' in res:  
      # get error
      result  = {
        "error" : res['error'], 
        "data" : None  
      }
    
    if 'publicKey' in res:
      # pubKey exists!
      pubKey = res['publicKey']
      result  = {
        "data" : pubKey
      }

    else:
      tmp = "{{Your account does not have public key!}}"
      tmp = _(tmp, lang)
      result  = {
        "error" : tmp, 
        "data" : None  
      }

    return json.dumps(result)

  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################

  def get_block_info(self, block):
    """ Get Block Info """

    url = """%s://%s/%s?requestType=getBlock&block=%s&includeTransactions=true&includeExecutedPhased=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, block )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
        "data" : None  
      }
      return json.dumps(result)
    
    if 'height' in res:
      # looks like block exits!

      result  = {
        "data" : res
      }
    else:
      tmp = "{{We are sorry. Something goes wrong :(}}"
      result  = {
        "error" : tmp, 
        "data" : None  
      }

    return json.dumps(result)

  ###############################################################################################################################################################################################
  def get_ledger(self, account):
    """ Get Ledger Info """

    url = """%s://%s/%s?requestType=getAccountLedger&account=%s&includeTransactions=false""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription']
      }
      return json.dumps(result)
    
    if 'entries' in res:
      # looks like block exits!

      result  = {
        "data" : res
      }
    else:
      tmp = "{{We are sorry. Something goes wrong :(}}"
      result  = {
        "error" : tmp
      }

    return json.dumps(result)

  ###############################################################################################################################################################################################

  def get_assets(self, account, lang='en'):
    """ Get all assets for the account """

    url = """%s://%s/%s?requestType=getAccountAssets&account=%s&includeAssetInfo=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )

    print ("""DEBUG: %s """ % url)
    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
      }
      return json.dumps(result)
    
    if 'accountAssets' in res:
      result  = {
        "data" : res['accountAssets']
      }

    else:
      tmp = "We are sorry. Something goes wrong :("
      result  = {
        "error" : tmp
      }

    return json.dumps(result)
 
###############################################################################################################################################################################################

  def get_currencies(self, account, lang='en'):
    """ Get all currencies for the account """

    url = """%s://%s/%s?requestType=getAccountCurrencies&account=%s&includeCurrencyInfo=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX, account )

    print ("""DEBUG: %s """ % url)
    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription'], 
      }
      return json.dumps(result)
    
    if 'accountCurrencies' in res:
      result  = {
        "data" : res['accountCurrencies']
      }

    else:
      tmp = "We are sorry. Something goes wrong :("
      result  = {
        "error" : tmp
      }

    return json.dumps(result)
 
###############################################################################################################################################################################################
  def send_money(self, chain,  recipient, publicKey, amountNQT, message, encrypt=0):
    """ generate Tx for sending money without broadcast """

    url = """%s://%s/%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, ARDOR_PREFIX )

   # print ("""DEBUG: %s """ % url)

    if encrypt == 0 :
      # unencrypted msg
      payload = {
        'requestType'     : 'sendMoney',
        'chain'           : chain,
        'recipient'       : recipient,
        'publicKey'       : publicKey,
        'feeNQT'          : -1,
        'feeRateNQTPerFXT': -1,
        'amountNQT'       : amountNQT,
        'deadline'        : 720,
        'broadcast'       : 'false',
        'message'         : message,
        'messageIsText'   : 'true',
        'phased'          : 'false'
      }
    else :
      payload = {
        'requestType'             : 'sendMoney',
        'chain'                   : chain,
        'recipient'               : recipient,
        'publicKey'               : publicKey,
        'feeNQT'                  : -1,
        'feeRateNQTPerFXT'        : -1,
        'amountNQT'               : amountNQT,
        'deadline'                : 720,
        'broadcast'               : 'false',
        'messageToEncrypt'        : message,
        'messageToEncryptIsText'  : 'true',
        'phased'                  : 'false'
      }


    print ("""URL: %s""" % url)
    print ("""PAYLOAD: %s""" % payload)

    res = self.post_json(url, payload)

    print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription']
      }
      return json.dumps(result)
    
    if 'transactionJSON' in res:
      # looks like all right!
      result  = {
        "data" : res
      }
    else:
      tmp = "{{We are sorry. Something goes wrong :(}}"
      result  = {
        "error" : tmp
      }

    return json.dumps(result)





