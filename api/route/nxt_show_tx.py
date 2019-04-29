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

class nxt_show_tx:
  def on_get(self, req, resp, tx, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    nxt = Nxt()
    ttx = nxt.get_tx_info(tx)
    ttx = json.loads(ttx)

    if 'data' in ttx:
      _t = ttx['data']


      if _t == None : 
        page = u"""
          <h3>{{Looks like wrong transaction ID}}</h3>
        """
        page2 = _(page, lang)

        result = { 
          'error' : None,
          'data'  : page2
        }
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

        return True



      _type = u"""%s""" % _t['type'] 
      _subtype = u"""%s""" % _t['subtype']

      _ttype = utils.get_nxt_transaction_description(_type, _subtype)


      _from = _t['senderRS']
      _fromurl = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( _from, _from ) 

      if 'recipientRS' in _t:
        _to = _t['recipientRS']
        _tourl = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( _to, _to ) 
      else:
        _to = "genesis account"
        _tourl = _to

      _amount = utils.nqt2nxt ( _t['amountNQT'] )
      _b_amount = utils.beauty_float ( _amount ) 

      _fee = utils.nqt2nxt ( _t['feeNQT'] )

      _confirmations = _t['confirmations']
      _confirmations_b = utils.beauty_int(_confirmations)

      _deadline = _t['deadline']
      _date = utils.timestamp2time( _t['timestamp'] )

      _block = _t['block']
      _blockurl = """<a href='/explorer/block-%s' target=_blank>%s</a> """ % ( _block, _block ) 

      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic transaction details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Type}}</td><td>%s</td></tr> 
          <tr><td>{{From}}</td><td>%s</td></tr> 
          <tr><td>{{To}}</td><td>%s</td></tr> 
          <tr><td>{{Amount}}</td><td>%s NXT</td></tr> 
          <tr><td>{{Fee}}</td><td>%s NXT</td></tr> 
          <tr><td>{{Confirmations}}</td><td>%s</td></tr> 
          <tr><td>{{Deadline}}</td><td>%s</td></tr> 
          <tr><td>{{Date}}</td><td>%s UTC</td></tr> 
          <tr><td>{{Block}}</td><td>%s</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % (_ttype, _fromurl, _tourl, _b_amount, _fee, _confirmations_b, _deadline, _date, _blockurl)

    #print ("""DEBUG: %s""" % page )

    if 'error' in ttx:
      #print ("""DEBUG: ERROR IN TTX???? %s""" % ttx['error'] )

      page = u"""%s""" % ttx['error']


    # translate
    page2 = _(page, lang)

    #print ("""DEBUG: %s""" % page2 )

    result = { 
      'error' : None,
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True

