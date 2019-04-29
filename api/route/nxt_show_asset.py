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

class nxt_show_asset:
  def on_get(self, req, resp, asset, lang='en'):
    """ show info about asset """
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    nxt = Nxt()

    ass = nxt.get_asset_info(asset);
    ass = json.loads(ass)

    if 'error' in ass:
      page = u"""%s""" % ass['error']

      result = { 
        'error' : None,
        'data'  : page
      }

      resp.body = json.dumps(result)
      resp.status = falcon.HTTP_200

      return True


    if 'data' in ass:
      _a = ass['data']

      if _a == None : 
        page = u"""
          <h3>{{Looks like wrong asset ID}}</h3>
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
      accRS_url = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( accRS, accRS ) 

      assName = _a['name']
      assDesc = _a['description']
      assTransfers = _a['numberOfTransfers']
      assTrades = _a['numberOfTrades']
      assAccounts = _a['numberOfAccounts']

      assDec = _a['decimals']
      assInitialQuantity = _a['initialQuantityQNT']
      assInitial_b = utils.beauty_asset ( assInitialQuantity, assDec, assName )

      assQuantity = _a['quantityQNT']
      assQuantity_b = utils.beauty_asset ( assQuantity, assDec, assName ) 
        
      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic asset details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Issuer}}</td><td>%s</td></tr> 
          <tr><td>{{Asset name}}</td><td>%s</td></tr> 
          <tr><td>{{Asset description}}</td><td>%s</td></tr> 
          <tr><td>{{Decimals}}</td><td>%s</td></tr> 
          <tr><td>{{Initial Quantity}}</td><td>%s</td></tr> 
          <tr><td>{{Quantity}}</td><td>%s</td></tr> 
          <tr><td>{{Number of accounts}}</td><td>%s</td></tr> 
          <tr><td>{{Total transfets}}</td><td>%s</td></tr> 
          <tr><td>{{Total trades}}</td><td>%s</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % ( accRS_url, assName, assDesc, assDec, assInitial_b, assQuantity_b, assAccounts, assTransfers, assTrades )


    if 'error' in ass:
      page = u"""%s""" % ass['error']


    page2 = _(page, lang)

    result = { 
      'error' : None,
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True

