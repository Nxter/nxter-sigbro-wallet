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

class nxt_show_currency:
  def on_get(self, req, resp, currency, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    nxt = Nxt()

    cur = nxt.get_currency_info(currency);
    cur = json.loads(cur)

    if 'error' in cur:
      page = u"""%s""" % ass['error']
      result = { 
        'error' : None,
        'data'  : page
      }

      resp.body = json.dumps(result)
      resp.status = falcon.HTTP_200

      return True


    if 'data' in cur:
      _a = cur['data']

      if _a == None : 
        page = u"""
          <h3>{{Looks like wrong currency code}}</h3>
        """
        page2 = _(page, lang)
        return page2

      curName = _a['name']
      curDesc = _a['description']

      curIssuer = _a['accountRS']
      curIssuer__url = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( curIssuer, curIssuer ) 

      curDecimal = _a['decimals']
      curID = _a['currency']
      curNumberTransfers = _a['numberOfTransfers']
      curNumberExchanges = _a['numberOfExchanges']
      curTypes = _a['types'] # list

      curInitialSupply = _a['initialSupply']
      curInitialSupply_b = utils.beauty_currency( curInitialSupply, curDecimal, currency.upper() )

      curCurrentSupply = _a['currentSupply']
      curCurrentSupply_b = utils.beauty_currency( curCurrentSupply, curDecimal, currency.upper() )


      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic currency details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Issuer}}</td><td>%s</td></tr> 
          <tr><td>{{Name}}</td><td>%s</td></tr> 
          <tr><td>{{Description}}</td><td>%s</td></tr> 
          <tr><td>{{Decimals}}</td><td>%s</td></tr> 
          <tr><td>{{Initial Supply}}</td><td>%s</td></tr> 
          <tr><td>{{Current Supply}}</td><td>%s</td></tr> 
          <tr><td>{{Number of transfers}}</td><td>%s</td></tr> 
          <tr><td>{{Number of exhcanges}}</td><td>%s</td></tr> 
          <tr><td>{{Types}}</td><td>%s</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % ( curIssuer__url, curName, curDesc, curDecimal, curInitialSupply_b, curCurrentSupply_b, curNumberTransfers, curNumberExchanges, "; ".join(curTypes)  )

    page2 = _(page, lang)

    result = { 
      'error' : None,
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True


