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

class nxt_show_block:
  def on_get(self, req, resp, block, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    nxt = Nxt()

    blk = nxt.get_block_info(block);
    blk = json.loads(blk)

    if 'error' in blk:
      page = u"""%s""" % blk['error']
      return page

    if 'data' in blk:
      _a = blk['data']

      if _a == None : 
        page = u"""
          <h3>{{Looks like wrong block ID}}</h3>
        """
        page2 = _(page, lang)

        result = { 
          'error' : None,
          'data'  : page2
        }
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

        return True


      blkGen = _a['generatorRS']
      blkGen_url = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( blkGen, blkGen ) 

      blkTransactionNumbers = _a['numberOfTransactions']

      blkTotalFee = _a['totalFeeNQT']
      blkTotalFee_b = utils.beauty_int( utils.nqt2nxt(  blkTotalFee ) )
      
      blkTotalAmount = _a['totalAmountNQT']
      blkTotalAmount_b = utils.beauty_float( utils.nqt2nxt( blkTotalAmount ) )

      blkTimestamp = _a['timestamp']
      blkTimestamp_b = utils.timestamp2time( blkTimestamp )

      if 'nextBlock' in _a:
        blkNext = _a['nextBlock']
        blkNext_url = """<a href='/explorer/block-%s' target=_self>%s</a> """ % ( blkNext, blkNext ) 
      else:
        blkNext_url = 'None'

      if 'previousBlock' in _a:
        blkPrev = _a['previousBlock']
        blkPrev_url = """<a href='/explorer/block-%s' target=_self>%s</a> """ % ( blkPrev, blkPrev ) 
      else:
        blkPrev_url = 'None'

      if 'height' in _a:
        blkHeight = _a['height']
      else:
        blkHeight = "Unknown"

      tr_list = {}

      if blkTransactionNumbers > 0 :
        transactions = _a['transactions']
        
        i = 0
        for tr in transactions:
          tr_list[i] = {'tr' : tr['transaction'], 'timestamp' : tr['timestamp'] }
          i = i + 1

        #print ("""DEBUG: %s """ % tr_list )
          
      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic block details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Block ID}}</td><td>%s</td></tr> 
          <tr><td>{{Block Height}}</td><td>%s</td></tr> 
          <tr><td>{{Block Generator}}</td><td>%s</td></tr> 
          <tr><td>{{Total Amount}}</td><td>%s NXT</td></tr> 
          <tr><td>{{Total Fee}}</td><td>%s NXT</td></tr> 
          <tr><td>{{Block Timestamp}}</td><td>%s UTC</td></tr> 
          <tr><td>{{Next Block}}</td><td>%s</td></tr> 
          <tr><td>{{Previous Block}}</td><td>%s</td></tr> 
          <tr><td>{{Include Transaction Numbers}}</td><td>%s</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % ( block, blkHeight, blkGen_url, blkTotalAmount_b, blkTotalFee_b, blkTimestamp_b, blkNext_url, blkPrev_url, blkTransactionNumbers )

      if len(tr_list) > 0: 
        page2_header = u"""
    <div class="nb container">
      <div class="nb row">
        <div class="nb col-xs-12 col-sm-12 col-md-12">
          <h4>{{Included transactions}}</h4>
          <table class="nb table table-striped">
        """
        page2_footer = u"""
          </table>
        </div>
      </div>
    </div>
        """ 

        page2_content = u""""""
        for i in tr_list:
          tr = tr_list[i]

          tr_url = """<a href='/explorer/tx-%s' target=_blank>%s</a>""" % ( tr['tr'], tr['tr'] )
          tr_time = utils.timestamp2time( tr['timestamp'] )

          page2_content = page2_content + u"""
            <tr><td>%s</td><td>%s</td></tr>
          """ % ( tr_time, tr_url )
          

        page = page + page2_header + page2_content + page2_footer


    page2 = _(page, lang)

    result = { 
      'error' : None,
      'data'  : page2
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True

