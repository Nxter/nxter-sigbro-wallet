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

class getWalletAssets:
  def on_get(self, req, resp, account, lang='en'):
    """ show info about assets for user """
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )

    nxt = Nxt()
    ard = Ardor()

    nxt_assets = nxt.get_assets(account);
    nxt_assets = json.loads(nxt_assets)

    ard_assets = ard.get_assets(account);
    ard_assets = json.loads(ard_assets);

    print (nxt_assets);
    print (ard_assets);

    # set error tag to Fals by default
    err1 = False
    err2 = False

    if 'error' in nxt_assets:
      err1 = True
      print ("""[%s][ERROR][NXT][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, nxt_assets['error']) )

    if 'error' in ard_assets:
      err2 = True
      print ("""[%s][ERROR][ARDOR][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, ard_assets['error']) )

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
            <p class="p-dgrey mb-0">Asset ID: %s</p>
            <a href="">Custom URL</a>
          </div>
        </div>
    </div>
    """

    page_nxt = u""""""
    page_ard = u""""""

    if 'data' in nxt_assets and len(nxt_assets['data']) > 0 :
      emp1 = False

      for ass in nxt_assets['data'] :
        name      = ass['name']
        ass_id    = ass['asset']
        quantity  = ass['quantityQNT']
        decimals  = ass['decimals']

        ass_quan  = utils.beauty_asset ( quantity, decimals, name )

        id1 = """heading_%s""" % ass_id 
        id2 = """collapse_%s""" % ass_id

        page_nxt = page_nxt + item % ( id1, id2, id2, 'nxt', name, ass_quan, id2, id1, ass_id )


    if 'data' in ard_assets and len(ard_assets['data']) > 0 :
      emp2 = False

      for ass in ard_assets['data'] :
        name      = ass['name']
        ass_id    = ass['asset']
        quantity  = ass['quantityQNT']
        decimals  = ass['decimals']

        ass_quan  = utils.beauty_asset ( quantity, decimals, name )

        id1 = """heading_%s""" % ass_id
        id2 = """collapse_%s""" % ass_id

        page_ard = page_ard + item % ( id1, id2, id2, 'ignis', name, ass_quan, id2, id1, ass_id )

    # if nxt & ardor got empty => show error msg
    if ( emp1 == True and emp2 == True ) :
      page = u"""
        <h3>{{You have not any Assets}}</h3>
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

