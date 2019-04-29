# -*- coding: UTF-8 -*-

from inc.nxt    import Nxt
from inc.ardor  import Ardor

from inc        import utils
from inc.local  import translate as _

from inc.model  import *

import json
import random
import hashlib
import falcon
import time
import re

# save or load unsigned JSON from DB

class getWalletJSON:
  def on_post(self, req, resp, url, lang='en'):
    resp.status = falcon.HTTP_405
    
  def on_get(self, req, resp, url, lang='en'):
    """ return unsignedJSON from database """

    try: 
      tx = WalletJSON.get( WalletJSON.url == url ).unsignedTX
    except Exception as e:
      print ("""[%s][ERROR][%s] Get record. [%s].""" % ( datetime.now(), self.__class__, e ) )       
      resp.status = falcon.HTTP_404
      return

    if len(tx) > 100 :
      resp.body = tx
      resp.status = falcon.HTTP_200
    else :
      resp.status = falcon.HTTP_404
    

class postWalletJSON:
  def on_get(self, req, resp):
    resp.status = falcon.HTTP_405

  def on_post(self, req, resp):
    """ save unsignedJSON into DB """
    data = req.bounded_stream.read()

    # generate url. use md5 because it is not secure data and will be unique for the same data..
    url = hashlib.md5(data).hexdigest()

    try :
      is_exists = WalletJSON.get( url == url )
    except :
      is_exists = 0

    if is_exists == 0 :
      try :
        WalletJSON.create( 
          timestamp = int(datetime.timestamp(datetime.now())),
          unsignedTX = data,
          url = url )

      except Exception as e :
        print ("""[%s][ERROR][%s] Add new record.[%s].""" % ( datetime.now(), self.__class__, e ) )       
        resp.body = json.dumps( { 'url' : '' } )
        resp.status = falcon.HTTP_200
        return

    full_url = u"""https://random.nxter.org/api/wallet/json/%s""" % url

    resp.body = json.dumps( { 'url' : full_url } )
    resp.status = falcon.HTTP_200



