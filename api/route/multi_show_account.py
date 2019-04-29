# -*- coding: UTF-8 -*-

from inc.ardor  import Ardor
from inc.nxt    import Nxt

from inc        import utils
from inc.local  import translate as _

import json
import random
import hashlib
import falcon
import time
import re

class multi_show_account:
  def on_get(self, req, resp, account, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    ardor = Ardor()
    nxt   = Nxt()

    account_ardor = """ARDOR-%s""" % account
    account_nxt   = """NXT-%s""" % account

    # load info about ardor
    acc_ardor = ardor.get_account_info_20180227(account_ardor)
    acc_ardor = json.loads(acc_ardor)

    # load info about nxt
    acc_nxt   = nxt.get_account_info(account_nxt)
    acc_nxt   = json.loads(acc_nxt)

    if 'error' in acc_nxt :
      accRS_nxt   = ''
      _b_accNxtBalance = ''
      acc_nxt_name = ''
      acc_nxt_desc = ''

      page = u"""%s""" % acc_nxt['error']

    if ( 'error' in acc_ardor) :
      accRS_ardor           = ''
      acc_ardor_name        = ''
      acc_ardor_desc        = ''
      _b_accArdrBalance     = ''
      _b_accIgnisBalance    = ''
      _b_accAeurBalance     = ''
      _b_accBitswiftBalance = ''

      page = u"""%s""" % acc_ardor['error']

    if ( 'data' in acc_nxt ) and  ( 'accountRS' in acc_nxt['data'] ) :
      acc_nxt = acc_nxt['data']

    ################################### ARDOR
    if ( 'accountRS' in acc_ardor ) :

      accRS_ardor = acc_ardor['accountRS']

      if 'name' in acc_ardor :
        acc_ardor_name = acc_ardor['name']
      else:
        acc_ardor_name = ''

      if 'description' in acc_ardor :
        acc_ardor_desc = acc_ardor['description']
      else:
        acc_ardor_desc = ''

      accArdrBalance = utils.nqt2ardr ( acc_ardor['ardorNQT'] )
      _b_accArdrBalance = utils.beauty_float ( accArdrBalance ) 

      accIgnisBalance = utils.nqt2ignis ( acc_ardor['ignisNQT'] )
      _b_accIgnisBalance = utils.beauty_float ( accIgnisBalance ) 

      accAeurBalance = utils.nqt2aeur ( acc_ardor['aeurNQT'] )
      _b_accAeurBalance = utils.beauty_float ( accAeurBalance ) 

      accBitswiftBalance = utils.nqt2bitswift ( acc_ardor['bitswiftNQT'] )
      _b_accBitswiftBalance = utils.beauty_float ( accBitswiftBalance ) 


    ############################### NXT
    if 'accountRS' in acc_nxt :
      accRS_nxt   = acc_nxt['accountRS']
      
      if 'name' in acc_nxt :
        acc_nxt_name = acc_nxt['name']
      else:
        acc_nxt_name = ''

      if 'description' in acc_nxt :
        acc_nxt_desc = acc_nxt['description']
      else:
        acc_nxt_desc = ''
      
      if 'balanceNQT' in acc_nxt :
        accNxtBalance = utils.nqt2nxt( acc_nxt['balanceNQT'] )
        _b_accNxtBalance = utils.beauty_float( accNxtBalance )
      else :
        _b_accNxtBalance = '---'

    
    ################################# GENERATE PAGE
     
    page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Ardor account details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{AccountRS}}</td><td>%s</td></tr> 
          <tr><td>{{Account name}}</td><td>%s</td></tr> 
          <tr><td>{{Account description}}</td><td>%s</td></tr> 
          <tr><td>{{Balance}}</td><td>%s ARDR</td></tr> 
          <tr><td>{{Balance}}</td><td>%s IGNIS</td></tr> 
          <tr><td>{{Balance}}</td><td>%s AEUR</td></tr> 
          <tr><td>{{Balance}}</td><td>%s BITSWIFT</td></tr> 
        </table>
      </div>

      <div class="nb col-xs-12 col-sm-12 col-md-12" id="nxter-bridge-explorer-ledger">
        <a href='#' id='nxter-bridge-explorer-load-ledger' data-account='%s' class='nb btn btn-primary'>Show Ledger</a>
      </div>

      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Nxt account details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{AccountRS}}</td><td>%s</td></tr> 
          <tr><td>{{Account name}}</td><td>%s</td></tr> 
          <tr><td>{{Account description}}</td><td>%s</td></tr> 
          <tr><td>{{Balance}}</td><td>%s NXT</td></tr> 
        </table>
      </div>

    </div>
  </div>
    """ % ( accRS_ardor, acc_ardor_name, acc_ardor_desc, _b_accArdrBalance, _b_accIgnisBalance, _b_accAeurBalance, _b_accBitswiftBalance, accRS_ardor, accRS_nxt, acc_nxt_name, acc_nxt_desc, _b_accNxtBalance )

    page2 = _(page, lang)

    result = { 
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True

