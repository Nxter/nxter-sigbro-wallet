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
import random
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


class Nxt():
  """ API for Explorer """

  def __init__(self):
    """ initialization """

  def __del__(self):
    """ destroing """

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
  ###############################################################################################################################################################################################

  def get_tx_info(self, tx):
    """Get Nxt transaction info"""
    url = """%s://%s/%s?requestType=getTransaction&transaction=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, tx )

    print ("""DEBUG: %s """ % url)
    res = self.get_json(url)

    if 'errorDescription' in res:  
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

  def get_account_info(self, account):
    """ Get Nxt Account Info """

    # try to get public key for the sender
    url = """%s://%s/?requestType=getAccount&account=%s&includeLessors=true&includeAssets=true&includeCurrencies=true&includeEffectiveBalance=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, account )

    print ("""DEBUG: %s """ % url)

    res = self.get_json(url)

    #print ("""DEBUG: %s """ % res )

    if 'errorDescription' in res:  
      # get error
      result  = {
        "error" : res['errorDescription']
      }
      return json.dumps(result)
    
    if 'balanceNQT' in res:
      # looks like transaction exits!

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
  ###############################################################################################################################################################################################

  def get_asset_info(self, asset):
    """ Get Asset Info """

    url = """%s://%s/%s?requestType=getAsset&asset=%s&includeCounts=true""" % ( DEFAULT_NODE_PROTO , DEFAULT_NODE_ADDRESS, NXT_PREFIX, asset )
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
    
    if 'name' in res:
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

  def get_block_info(self, block):
    """ Get Block Info """

    url = """%s://%s/%s?requestType=getBlock&block=%s&includeTransactions=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, block )

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
  ###############################################################################################################################################################################################

  def get_currency_info(self, currency, lang='en'):
    """ Get Currency Info """

    url = """%s://%s/%s?requestType=getCurrency&code=%s&includeCounts=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, currency )

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
    
    if 'code' in res:
      result  = {
        "data" : res
      }

    else:
      tmp = "{{We are sorry. Something goes wrong :(}}"
      tmp = _(tmp, lang)
      result  = {
        "error" : tmp, 
        "data" : None  
      }

    return json.dumps(result)
 

  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################
  def get_public_key(self, sender):
    """ Get Public Key"""

    pubKey = ''
    # try to get public key for the sender
    url = """%s://%s/%s?requestType=getAccountPublicKey&account=%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, sender )
    print ("""DEBUG: %s """ % url)

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

  def get_assets(self, account, lang='en'):
    """ Get all assets for the account """

    url = """%s://%s/%s?requestType=getAccountAssets&account=%s&includeAssetInfo=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, account )

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

    url = """%s://%s/%s?requestType=getAccountCurrencies&account=%s&includeCurrencyInfo=true""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX, account )

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
  def send_money(self,  recipient, publicKey, amountNQT, feeNQT, message, encrypt=0):
    """ generate Tx for sending money without broadcast """

    url = """%s://%s/%s""" % ( DEFAULT_NODE_PROTO, DEFAULT_NODE_ADDRESS, NXT_PREFIX )

   # print ("""DEBUG: %s """ % url)

    if encrypt == 0 :
      # unencrypted 
      payload = {
        'requestType'     : 'sendMoney',
        'recipient'       : recipient,
        'publicKey'       : publicKey,
        'feeNQT'          : feeNQT,
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
        'recipient'               : recipient,
        'publicKey'               : publicKey,
        'feeNQT'                  : feeNQT,
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

  ###############################################################################################################################################################################################

