# -*- coding: UTF-8 -*-

import math
import time
import datetime
import random
import json
import re

from __init__ import NXT_GENESIS_TIME
from __init__ import ARDOR_GENESIS_TIME

def nqt2nxt(nqt):
  """ conver NQT to NXT """
  return float(nqt) / math.pow(10,8) 

def nqt2ardr(nqt):
  """ conver NQT to ARDR """
  return float(nqt) / math.pow(10,8) 

def nqt2ignis(nqt):
  """ conver NQT to IGNIS """
  return float(nqt) / math.pow(10,8) 

def nqt2aeur(nqt):
  """ conver NQT to AEUR """
  return float(nqt) / math.pow(10,4) 

def nqt2bitswift(nqt):
  """ conver NQT to BITSWIFT """
  return float(nqt) / math.pow(10,8) 

def nxt2nqt(nxt):
  """ convert NXT to NQT """
  return int (float(nxt) * math.pow(10,8) )

def beauty_float(digit):
  """ show digit with dots and spaces """
  return "{0:,.2f}".format(float(digit)).replace(',', ' ')

def beauty_int(digit):
  """ show digit with dots and spaces """
  return "{0:,.0f}".format(float(digit)).replace(',', ' ')

def beauty_asset(amount, decimals, name):
  """ return converted asset """
  a = float(amount) / math.pow(10, decimals)
  b = "{0:,.0f}".format(float(a)).replace(',', ' ') 
  res = """%s %s""" % ( b, name )
  return res

def beauty_currency(amount, decimals, name):
  """ return converted asset """
  a = float(amount) / math.pow(10, decimals)
  b = "{0:,.0f}".format(float(a)).replace(',', ' ') 
  res = """%s %s""" % ( b, name )
  return res

def timestamp2time(timestamp):
  """ convert NXT timestamp into time """
  _ts = int(timestamp) + int(NXT_GENESIS_TIME)
  _tm = datetime.datetime.fromtimestamp(_ts)
  return _tm

def timestamp2ardortime(timestamp):
  """ convert ARDOR timestamp into time """
  _ts = int(timestamp) + int(ARDOR_GENESIS_TIME)
  _tm = datetime.datetime.fromtimestamp(_ts)
  return _tm

def nqt2chain(chain, nqt):
  """Convert into chain specific format"""
  if chain == 1 :
    return nqt2ardr(nqt)

  if chain == 2 :
    return nqt2ignis(nqt)

  if chain == 3 :
    return nqt2aeur(nqt)

  if chain == 4 :
    return nqt2bitswift(nqt)

  return nqt2ardr(nqt)

def get_chain_name(chain) :
  name = 'Unknown'

  if chain == 1 :
    name = "ARDR"
  if chain == 2 :
    name = "IGNIS"
  if chain == 3 :
    name = "AEUR"
  if chain == 4 :
    name = "BITSWIFT"

  return name

def get_nxt_transaction_description(tx_type, tx_subtype):
  """ return transaction type by type + subtype """

  #print ("""DEBUG. tx_type : %s, tx_subtype : %s """ % ( tx_type, tx_subtype ) )

  nxt_consts = json.loads("""{
  "genesisAccountId":"1739068987193023818",
  "transactionTypes":{
    "0":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":true,
          "name":"OrdinaryPayment",
          "canHaveRecipient":true,
          "type":0,
          "isPhasingSafe":true
        }
      }
    },
    "1":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"ArbitraryMessage",
          "canHaveRecipient":true,
          "type":1,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"AliasAssignment",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"PollCreation",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"VoteCasting",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":false
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"HubAnnouncement",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":true
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"AccountInfo",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":true
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":false,
          "name":"AliasSell",
          "canHaveRecipient":true,
          "type":1,
          "isPhasingSafe":false
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":true,
          "name":"AliasBuy",
          "canHaveRecipient":true,
          "type":1,
          "isPhasingSafe":false
        },
        "8":{
          "isPhasable":true,
          "subtype":8,
          "mustHaveRecipient":false,
          "name":"AliasDelete",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":false
        },
        "9":{
          "isPhasable":true,
          "subtype":9,
          "mustHaveRecipient":false,
          "name":"PhasingVoteCasting",
          "canHaveRecipient":false,
          "type":1,
          "isPhasingSafe":true
        },
        "10":{
          "isPhasable":true,
          "subtype":10,
          "mustHaveRecipient":true,
          "name":"AccountProperty",
          "canHaveRecipient":true,
          "type":1,
          "isPhasingSafe":true
        },
        "11":{
          "isPhasable":true,
          "subtype":11,
          "mustHaveRecipient":true,
          "name":"AccountPropertyDelete",
          "canHaveRecipient":true,
          "type":1,
          "isPhasingSafe":true
        }
      }
    },
    "2":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"AssetIssuance",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":true,
          "name":"AssetTransfer",
          "canHaveRecipient":true,
          "type":2,
          "isPhasingSafe":true
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"AskOrderPlacement",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":true
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"BidOrderPlacement",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":true
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"AskOrderCancellation",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":true
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"BidOrderCancellation",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":true
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":false,
          "name":"DividendPayment",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":false
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":false,
          "name":"AssetDelete",
          "canHaveRecipient":false,
          "type":2,
          "isPhasingSafe":true
        }
      }
    },
    "3":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsListing",
          "canHaveRecipient":false,
          "type":3,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsDelisting",
          "canHaveRecipient":false,
          "type":3,
          "isPhasingSafe":true
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsPriceChange",
          "canHaveRecipient":false,
          "type":3,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsQuantityChange",
          "canHaveRecipient":false,
          "type":3,
          "isPhasingSafe":false
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsPurchase",
          "canHaveRecipient":true,
          "type":3,
          "isPhasingSafe":false
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsDelivery",
          "canHaveRecipient":true,
          "type":3,
          "isPhasingSafe":false
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsFeedback",
          "canHaveRecipient":true,
          "type":3,
          "isPhasingSafe":false
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsRefund",
          "canHaveRecipient":true,
          "type":3,
          "isPhasingSafe":false
        }
      }
    },
    "4":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":true,
          "name":"EffectiveBalanceLeasing",
          "canHaveRecipient":true,
          "type":4,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"SetPhasingOnly",
          "canHaveRecipient":false,
          "type":4,
          "isPhasingSafe":false
        }
      }
    },
    "5":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"CurrencyIssuance",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"ReserveIncrease",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"ReserveClaim",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":true,
          "name":"CurrencyTransfer",
          "canHaveRecipient":true,
          "type":5,
          "isPhasingSafe":false
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"PublishExchangeOffer",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"ExchangeBuy",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":false,
          "name":"ExchangeSell",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":false,
          "name":"CurrencyMinting",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        },
        "8":{
          "isPhasable":true,
          "subtype":8,
          "mustHaveRecipient":false,
          "name":"CurrencyDeletion",
          "canHaveRecipient":false,
          "type":5,
          "isPhasingSafe":false
        }
      }
    },
    "6":{
      "subtypes":{
        "0":{
          "isPhasable":false,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"TaggedDataUpload",
          "canHaveRecipient":false,
          "type":6,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":false,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"TaggedDataExtend",
          "canHaveRecipient":false,
          "type":6,
          "isPhasingSafe":false
        }
      }
    },
    "7":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"ShufflingCreation",
          "canHaveRecipient":false,
          "type":7,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"ShufflingRegistration",
          "canHaveRecipient":false,
          "type":7,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":false,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"ShufflingProcessing",
          "canHaveRecipient":false,
          "type":7,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":false,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"ShufflingRecipients",
          "canHaveRecipient":false,
          "type":7,
          "isPhasingSafe":false
        },
        "4":{
          "isPhasable":false,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"ShufflingVerification",
          "canHaveRecipient":false,
          "type":7,
          "isPhasingSafe":false
        },
        "5":{
          "isPhasable":false,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"ShufflingCancellation",
          "canHaveRecipient":false,
          "type":7,
          "isPhasingSafe":false
        }
      }
    }
    }  
  }""")
  
  try:
    # tt - just a name from json without spaces
    tt = nxt_consts["transactionTypes"][tx_type]["subtypes"][tx_subtype]["name"] 
    # add space after Big Letter
    tt_beauty = re.sub( r"(\w)([A-Z])", r"\1 \2", tt )
  except KeyError :
    tt_beauty = "Unknown Type"
  
  return tt_beauty


def get_ardor_transaction_description(tx_type, tx_subtype):
  """ return transaction type by type + subtype """

  #print ("""DEBUG. tx_type : %s, tx_subtype : %s """ % ( tx_type, tx_subtype ) )

  ardor_consts = json.loads("""{
  "transactionTypes":{
    "0":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":true,
          "name":"OrdinaryPayment",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":0,
          "isPhasingSafe":true
        }
      }
    },
    "-1":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"ChildChainBlock",
          "canHaveRecipient":false,
          "type":-1,
          "isPhasingSafe":true
        }
      }
    },
    "1":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"ArbitraryMessage",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":1,
          "isPhasingSafe":false
        }
      }
    },
    "-2":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":true,
          "name":"FxtPayment",
          "canHaveRecipient":true,
          "type":-2,
          "isPhasingSafe":true
        }
      }
    },
    "2":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"AssetIssuance",
          "canHaveRecipient":false,
          "isGlobal":true,
          "type":2,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":true,
          "name":"AssetTransfer",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":true
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"AskOrderPlacement",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":true
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"BidOrderPlacement",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":true
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"AskOrderCancellation",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":true
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"BidOrderCancellation",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":true
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":false,
          "name":"DividendPayment",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":false
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":false,
          "name":"AssetDelete",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":2,
          "isPhasingSafe":true
        },
        "8":{
          "isPhasable":true,
          "subtype":8,
          "mustHaveRecipient":false,
          "name":"AssetIncrease",
          "canHaveRecipient":false,
          "isGlobal":true,
          "type":2,
          "isPhasingSafe":false
        },
        "9":{
          "isPhasable":true,
          "subtype":9,
          "mustHaveRecipient":false,
          "name":"SetPhasingAssetControl",
          "canHaveRecipient":false,
          "isGlobal":true,
          "type":2,
          "isPhasingSafe":false
        }
      }
    },
    "-3":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":true,
          "name":"EffectiveBalanceLeasing",
          "canHaveRecipient":true,
          "type":-3,
          "isPhasingSafe":true
        }
      }
    },
    "3":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsListing",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsDelisting",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":true
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsPriceChange",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"DigitalGoodsQuantityChange",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":false
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsPurchase",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":false
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsDelivery",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":false
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsFeedback",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":false
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":true,
          "name":"DigitalGoodsRefund",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":3,
          "isPhasingSafe":false
        }
      }
    },
    "-4":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"FxtCoinExchangeOrderIssue",
          "canHaveRecipient":false,
          "type":-4,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"FxtCoinExchangeOrderCancel",
          "canHaveRecipient":false,
          "type":-4,
          "isPhasingSafe":true
        }
      }
    },
    "4":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"SetPhasingOnly",
          "canHaveRecipient":false,
          "isGlobal":true,
          "type":4,
          "isPhasingSafe":false
        }
      }
    },
    "5":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"CurrencyIssuance",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"ReserveIncrease",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"ReserveClaim",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":true
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":true,
          "name":"CurrencyTransfer",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":true
        },
        "4":{
          "isPhasable":true,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"PublishExchangeOffer",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":true
        },
        "5":{
          "isPhasable":true,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"ExchangeBuy",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":true
        },
        "6":{
          "isPhasable":true,
          "subtype":6,
          "mustHaveRecipient":false,
          "name":"ExchangeSell",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":true
        },
        "7":{
          "isPhasable":true,
          "subtype":7,
          "mustHaveRecipient":false,
          "name":"CurrencyMinting",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":false
        },
        "8":{
          "isPhasable":true,
          "subtype":8,
          "mustHaveRecipient":false,
          "name":"CurrencyDeletion",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":5,
          "isPhasingSafe":false
        }
      }
    },
    "6":{
      "subtypes":{
        "0":{
          "isPhasable":false,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"TaggedDataUpload",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":6,
          "isPhasingSafe":false
        }
      }
    },
    "7":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"ShufflingCreation",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":7,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"ShufflingRegistration",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":7,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":false,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"ShufflingProcessing",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":7,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":false,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"ShufflingRecipients",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":7,
          "isPhasingSafe":false
        },
        "4":{
          "isPhasable":false,
          "subtype":4,
          "mustHaveRecipient":false,
          "name":"ShufflingVerification",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":7,
          "isPhasingSafe":false
        },
        "5":{
          "isPhasable":false,
          "subtype":5,
          "mustHaveRecipient":false,
          "name":"ShufflingCancellation",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":7,
          "isPhasingSafe":false
        }
      }
    },
    "8":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"AliasAssignment",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":8,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"AliasSell",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":8,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":true,
          "name":"AliasBuy",
          "canHaveRecipient":true,
          "isGlobal":false,
          "type":8,
          "isPhasingSafe":false
        },
        "3":{
          "isPhasable":true,
          "subtype":3,
          "mustHaveRecipient":false,
          "name":"AliasDelete",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":8,
          "isPhasingSafe":false
        }
      }
    },
    "9":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"PollCreation",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":9,
          "isPhasingSafe":false
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"VoteCasting",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":9,
          "isPhasingSafe":false
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":false,
          "name":"PhasingVoteCasting",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":9,
          "isPhasingSafe":true
        }
      }
    },
    "10":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"AccountInfo",
          "canHaveRecipient":false,
          "isGlobal":true,
          "type":10,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":true,
          "name":"AccountProperty",
          "canHaveRecipient":true,
          "isGlobal":true,
          "type":10,
          "isPhasingSafe":true
        },
        "2":{
          "isPhasable":true,
          "subtype":2,
          "mustHaveRecipient":true,
          "name":"AccountPropertyDelete",
          "canHaveRecipient":true,
          "isGlobal":true,
          "type":10,
          "isPhasingSafe":true
        }
      }
    },
    "11":{
      "subtypes":{
        "0":{
          "isPhasable":true,
          "subtype":0,
          "mustHaveRecipient":false,
          "name":"CoinExchangeOrderIssue",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":11,
          "isPhasingSafe":true
        },
        "1":{
          "isPhasable":true,
          "subtype":1,
          "mustHaveRecipient":false,
          "name":"CoinExchangeOrderCancel",
          "canHaveRecipient":false,
          "isGlobal":false,
          "type":11,
          "isPhasingSafe":true
        }
      }
    }
    }
  }""")

  try:
    # tt - just a name from json without spaces
    tt = ardor_consts["transactionTypes"][tx_type]["subtypes"][tx_subtype]["name"] 
    # add space after Big Letter
    tt_beauty = re.sub( r"(\w)([A-Z])", r"\1 \2", tt )
  except KeyError :
    tt_beauty = "Unknown Type"
  
  return tt_beauty




