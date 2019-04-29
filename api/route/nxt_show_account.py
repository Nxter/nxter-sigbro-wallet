# -*- coding: UTF-8 -*-

from inc.nxt    import Nxt
from inc        import utils
from inc.local  import translate as _

import json
import random
import hashlib
import falcon
import time
import re

class nxt_show_account:
  def on_get(self, req, resp, account, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    nxt = Nxt()

    acc = nxt.get_account_info(account);
    acc = json.loads(acc)

    if 'data' in acc:
      _a = acc['data']

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
        
      accBalance = utils.nqt2nxt ( _a['balanceNQT'] )
      _b_accBalance = utils.beauty_float ( accBalance ) 

      accID = _a['account']

      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic account details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Account name}}</td><td>%s</td></tr> 
          <tr><td>{{Account description}}</td><td>%s</td></tr> 
          <tr><td>{{AccountRS}}</td><td>%s</td></tr> 
          <tr><td>{{Account numeric}}</td><td>%s</td></tr> 
          <tr><td>{{Balance}}</td><td>%s NXT</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % ( accName, accDesc, accRS, accID, _b_accBalance )

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

