# -*- coding: UTF-8 -*-

from inc.nxt    import Nxt
from inc.ardor  import Ardor

from inc        import utils
from inc.local  import translate as _

import json
import random
import hashlib
import falcon
import time
import re

class getWalletCurrencies:
  def on_get(self, req, resp, account, lang='en'):
    """ show info about currencies for user """
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )

    nxt = Nxt()
    ard = Ardor()

    nxt_curr = nxt.get_currencies(account);
    nxt_curr = json.loads(nxt_curr)

    ard_curr = ard.get_currencies(account);
    ard_curr = json.loads(ard_curr);

    print (nxt_curr);
    print (ard_curr);

    # set error tag to Fals by default
    err1 = False
    err2 = False

    if 'error' in nxt_curr:
      err1 = True
      print ("""[%s][ERROR][NXT][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, nxt_curr['error']) )

    if 'error' in ard_curr:
      err2 = True
      print ("""[%s][ERROR][ARDOR][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, ard_curr['error']) )

    # if nxt & ardor got false => show error msg
    if ( err1 == True and err2 == True ) :
      page = u"""
        <h3>{{Something goes wrong}}</h3>
      """
      result = { 'data' : page }

      resp.body = json.dumps(result)
      resp.status = falcon.HTTP_200
      return

    # set empty tag for True by default
    emp1 = True
    emp2 = True

    # 1 - div ID1 (headingOne)
    # 2 - div ID2 (collapseOne) 
    # 3 - div ID2 (collapseOne)
    # 4 - IMG NAME (nxt, ignis)
    # 5 - Asset Name
    # 6 - Asset Amount
    # 7 - div ID2 (collapseOne)
    # 8 - div ID1 (headingOne)
    # 9 - Asset ID

    item = u"""
      <div class="collapse-block">
        <div class="balance-stroke" id="%s">
          <a class="collapsed a-black" role="button" data-toggle="collapse" data-parent="#accordion" href="#%s" aria-expanded="false" aria-controls="%s">
            <div class="logo-crypto-box"><img src="img/%s.png" alt="" class="logo-crypto"></div>
            <p class="p-crypto-name text-uppercase">%s</p>
            <p class="p-balance float-right"><b>%s</b><i class="p-grey more-less icon-fontello icon-plus"></i></p>
          </a>
        </div>

        <div id="%s" class="collapse" aria-labelledby="%s" data-parent="#accordionAssets">
          <div class="card-body">
            <p class="p-dgrey mb-0">Currency ID: %s</p>
            <a href="">Custom URL</a>
            <p class="p-property d-inline">TYPE 1</p>
            <p class="p-property d-inline">TYPE 2</p>
          </div>
        </div>
    </div>
    """

    page_nxt = u""""""
    page_ard = u""""""

    if 'data' in nxt_curr and len(nxt_curr['data']) > 0 :
      emp1 = False

      for curr in nxt_curr['data'] :
        curr_id   = curr['currency']
        name      = curr['name']
        code      = curr['code']
        issuer    = curr['issuerAccountRS']
        decimals  = curr['decimals']
        units     = curr['units']

        cur_amount  = utils.beauty_asset ( units, decimals, code )

        id1 = """heading_%s""" % curr_id
        id2 = """collapse_%s""" % curr_id

        page_nxt = page_nxt + item % ( id1, id2, id2, 'nxt', name, cur_amount, id2, id1, curr_id )


    if 'data' in ard_curr and len(ard_curr['data']) > 0 :
      emp2 = False

      for curr in ard_curr['data'] :
        curr_id   = curr['currency']
        name      = curr['name']
        code      = curr['code']
        issuer    = curr['issuerAccountRS']
        decimals  = curr['decimals']
        units     = curr['unitsQNT']

        cur_amount  = utils.beauty_asset ( units, decimals, code )

        id1 = """heading_%s""" % curr_id
        id2 = """collapse_%s""" % curr_id

        page_ard = page_ard + item % ( id1, id2, id2, 'ignis', name, cur_amount, id2, id1, curr_id )

    # if nxt & ardor got empty => show error msg
    if ( emp1 == True and emp2 == True ) :
      page = u"""
        <h3>{{You have not any Currencies}}</h3>
      """
      page2 = _(page, lang)
      result = { 'data' : page2 }

      resp.body = json.dumps(result)
      resp.status = falcon.HTTP_200
      return

    page = page_nxt + page_ard
    page2 = _(page, lang)

    result = { 
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True

