# -*- coding: UTF-8 -*-

from inc.nxt    import Nxt
from inc.ardor  import Ardor

from inc        import utils
from inc.local  import translate as _

from inc.model  import *

import requests
import json
import random
import hashlib
import falcon
import time
import re

class postWalletSendMoney:
  def post_json(self, url, payload):
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

  def save_it_external(self, data):
    """ save json to remove server http://random.nxter.org/api/v3/save_tx """
    url = """https://random.nxter.org/api/v3/save_tx"""

    res = self.post_json(url, data);

    if 'error' in res :
      print ("""[%s][ERROR][%s] Save json remotely. [%s].""" % ( datetime.now(), self.__class__, res['error'] ) )       
      return json.dumps( { 'url' : '', 'error' : res['error'] } )

    # correct response {"msg":"Transaction saved","result":"ok","uuid":"4e17b00a-38c2-42e8-9382-eb7690281c73"}

    if 'uuid' in res:
      print ("""[%s][INFO][%s] Save json success. [%s].""" % ( datetime.now(), self.__class__, res['uuid'] ) )       
      full_url = u"""https://random.nxter.org/api/v3/load_tx/%s""" % res['uuid']
      return json.dumps( { 'url' : full_url } )

    if 'msg' in res :
      print ("""[%s][DEBUG][%s] Save json remotely. [%s].""" % ( datetime.now(), self.__class__, res['msg'] ) )       
      return json.dumps( { 'url' : '', 'error' : res['msg'] } )


  def save_it(self, data) :
    """save unsigned JSON into db and returl URL"""
    data = data.encode()
    url = hashlib.md5(data).hexdigest()

    print ("""[%s][DEBUG][%s] URL: [%s].""" % ( datetime.now(), self.__class__, url ) )       
    

    is_exists = None
    try :
      is_exists = WalletJSON.get_or_none( WalletJSON.url == url )
    except :
      is_exists = None
      pass

    print ("""[%s][DEBUG][%s] IS_EXIST: [%s].""" % ( datetime.now(), self.__class__, is_exists ) )       


    if is_exists == None :
      try :
        print ("""[%s][DEBUG][%s] start adding record for [%s].""" % ( datetime.now(), self.__class__, url ) )       
        WalletJSON.create( 
          timestamp = int(datetime.timestamp(datetime.now())),
          unsignedTX = data,
          url = url )
        print ("""[%s][DEBUG][%s] end adding record for [%s].""" % ( datetime.now(), self.__class__, url ) )       

      except Exception as e :
        print ("""[%s][ERROR][%s] Add new record.[%s].""" % ( datetime.now(), self.__class__, e ) )       
        return json.dumps( { 'url' : '' } )

    full_url = u"""https://random.nxter.org/api/wallet/json/%s""" % url

    return json.dumps( { 'url' : full_url } )


  def on_get(self, req, resp): resp.status = falcon.HTTP_405

  def on_post(self, req, resp):
    """ generate send money transaction """
    data = req.bounded_stream.read()

    try :
      data_j = json.loads(data)
    except Exception as e :
      print ("""[%s][ERROR][%s] Parse JSON data. [%s].""" % ( datetime.now(), self.__class__, e ) )       
      resp.status = falcon.HTTP_400 # Bad Request
      return

    print ("""[%s][DEBUG][%s] Request: [%s] """ % ( datetime.now(), self.__class__, data_j ) )       
    # checking all params
    if ( 'currencie' not in data_j ) or ('recipient' not in data_j) or ('amount' not in data_j) or ('publicKey' not in data_j) or ( 'fee' not in data_j ) :
      print ("""[%s][INFO][%s] Wrong params amount. """ % ( datetime.now(), self.__class__ ) )       
      resp.body = json.dumps( { 'error' : 'Wrong params amount.' } )
      resp.status = falcon.HTTP_200
      return


    ########## NXT
    if data_j['currencie'] == 'nxt' :
      crypto = Nxt()

      # 0 -- plain text, 1 - encrypt
      encrypt = 0
      if 'encrypt_msg' in data_j :
        encrypt = data_j['encrypt_msg']


      # fee for unencrypt msg is 1NXT, for encrypt = 3 NXT

      fee = data_j['fee']

      if encrypt == 0 :
        # 1 NXT by default
        fee = int(1) * pow(10,8)
      else :
        # 3 NXT
        fee = int(3) * pow(10,8)

      try :
        amount = float(data_j['amount']) * pow(10,8)
      except :
        amount = 1


      amount = int(amount)
      fee = int(fee)

      msg = None
      if 'msg' in data_j :
        msg = data_j['msg']
      else :
        msg = ''


      tx = crypto.send_money( data_j['recipient'], data_j['publicKey'], amount, fee, msg, encrypt )

      rez_url = None
      rez     = None

      try :
        tx = json.loads(tx)
      except :
        pass

      if 'data' in tx :
        # correct response
        print ("""[DEBUG][RESPONZE] %s """ % tx['data'] )

        responze = tx['data']

        # TODO change to external API /api/v3/save_tx and send all info
        if 'transactionJSON' in responze :
          rez_url = self.save_it_external( json.dumps(responze) )

      else :
        rez = tx 
        
    else :
      ####### NOT NXT
      decimals = None
      chain = None
      crypto = Ardor()

      # 0 -- plain text, 1 - encrypt
      encrypt = 0
      if 'encrypt_msg' in data_j :
        encrypt = data_j['encrypt_msg']

      if data_j['currencie'] == 'ardor' :
        ################# ARDOR
        decimals = 8
        chain = 1
      if data_j['currencie'] == 'ignis' :
        ################# IGNIS
        decimals = 8
        chain = 2
      if data_j['currencie'] == 'aeur' :
        decimals = 4
        chain = 3
      if data_j['currencie'] == 'bitswift' :
        decimals = 8
        chain = 4


      fee = data_j['fee']
      # always auto-fee
      if fee == -1 :
        fee = int(-1)
      else :
        fee = int(-1)

      try :
        amount = float(data_j['amount']) * pow(10,decimals)
      except :
        amount = 1


      amount = int(amount)
      fee = int(fee)

      msg = None
      if 'msg' in data_j :
        msg = data_j['msg']
      else :
        msg = ''

      # 1 -- ARDOR
      tx = crypto.send_money( chain, data_j['recipient'], data_j['publicKey'], amount, msg, encrypt )

      rez_url = None
      rez     = None

      try :
        tx = json.loads(tx)
      except :
        pass

      if 'data' in tx :
        # correct response
        print ("""[DEBUG][RESPONZE] %s """ % tx['data'] )

        responze = tx['data']

        # TODO change to new API /api/v3/save_tx
        if 'transactionJSON' in responze :
          rez_url = self.save_it_external( json.dumps(responze) )

      else :
        rez = tx 

    if rez_url is not None :
      # if url in responze
      resp.body = rez_url
    else :
      # if error in responze
      resp.body = json.dumps( rez )

    resp.status = falcon.HTTP_200



