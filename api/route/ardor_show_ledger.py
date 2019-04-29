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

class ardor_show_ledger:
  def on_get(self, req, resp, account, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    ardor = Ardor()

    try :
      ttx = ardor.get_ledger(account);
      ttx = json.loads(ttx)
    except Exception as e :
      result = { 
        'error' : e
      }
      resp.body = json.dumps(result)
      resp.status = falcon.HTTP_200
      return True
 
    if 'data' in ttx:
      _t = ttx['data']

      page_start = u"""
        <h4>{{Ardor Ledger}}</h4>
        <hr>
        <table class="nb table table-striped">
        <thead>
          <tr>
            <td>Date</td><td>Type</td><td>Chain</td><td>Change</td><td>Balance</td>
          </tr>
        </thead>
        """
      page_end = u"""
        </table>
      """ 

      page_middle = u""""""

      if 'entries' in _t :
        entries = _t['entries']

        for ent in entries :
          chain   = None
          date    = None
          change  = None
          balance = None
          etype   = None

          if 'chain' in ent :
            chain = ent['chain']
          if 'timestamp' in ent :
            date = ent['timestamp']
          if 'change' in ent:
            change = ent['change']
          if 'balance' in ent:
            balance = ent['balance']
          if 'eventType' in ent:
            etype = ent['eventType']

          if chain == None or date == None or change == None or balance == None or etype == None :
            continue

          _chain = utils.get_chain_name(chain)
          _date  = utils.timestamp2ardortime(date)
          _etype = etype.lower().replace("_"," ").title()
          _change = utils.nqt2chain(chain, change)
          _balance = utils.nqt2chain(chain, balance)

          row = """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % ( _date, _etype, _chain, _change, _balance )

          page_middle = page_middle + row

      page3 = page_start + page_middle + page_end

    if 'error' in ttx:
      page3 = u"""%s""" % ttx['error']

    page4 = _(page3, lang)

    result = { 
      'data'  : page4
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200


    return True


  ###############################################################################################################################################################################################

