# -*- coding: UTF-8 -*-

from inc.ardor  import Ardor
from inc        import utils
from inc.local  import translate as _

import json
import random
import hashlib
import falcon
import time
import re

class ardor_show_account:
  def on_get(self, req, resp, account, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    ardor = Ardor()

    acc = ardor.get_account_info(account);
    acc = json.loads(acc)

    if 'accountRS' in acc:
      _a = acc

      if _a == None : 
        page = u"""
          <h3>{{Looks like wrong account number}}</h3>
        """
        page2 = _(page, lang)

        result = { 
          'error' : None,
          'data'  : page2
        }
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

        return True

      accRS = _a['accountRS']

      if 'name' in _a :
        accName = _a['name']
      else:
        accName = ''

      if 'description' in _a :
        accDesc = _a['description']
      else:
        accDesc = ''
        
      accArdrBalance = utils.nqt2ardr ( _a['ardorNQT'] )
      _b_accArdrBalance = utils.beauty_float ( accArdrBalance ) 

      accIgnisBalance = utils.nqt2ignis ( _a['ignisNQT'] )
      _b_accIgnisBalance = utils.beauty_float ( accIgnisBalance ) 

      accAeurBalance = utils.nqt2aeur ( _a['aeurNQT'] )
      _b_accAeurBalance = utils.beauty_float ( accAeurBalance ) 

      accBitswiftBalance = utils.nqt2bitswift ( _a['bitswiftNQT'] )
      _b_accBitswiftBalance = utils.beauty_float ( accBitswiftBalance ) 

      accID = account

      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic account details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Account name}}</td><td>%s</td></tr> 
          <tr><td>{{Account description}}</td><td>%s</td></tr> 
          <tr><td>{{AccountRS}}</td><td>%s</td></tr> 
          <tr><td>{{Balance}}</td><td>%s ARDR</td></tr> 
          <tr><td>{{Balance}}</td><td>%s IGNIS</td></tr> 
          <tr><td>{{Balance}}</td><td>%s AEUR</td></tr> 
          <tr><td>{{Balance}}</td><td>%s BITSWIFT</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % ( accName, accDesc, accRS, _b_accArdrBalance, _b_accIgnisBalance, _b_accAeurBalance, _b_accBitswiftBalance )

    if 'error' in acc:
      page = u"""%s""" % acc['error']

    page2 = _(page, lang)

    result = { 
      'error' : None,
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200


    return True

