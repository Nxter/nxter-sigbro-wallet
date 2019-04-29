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

class ardor_show_fxt:
  def on_get(self, req, resp, fxt, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    ardor = Ardor()

    ttx = ardor.get_fxt_info(fxt);
    ttx = json.loads(ttx)

    if 'data' in ttx:
      _t = ttx['data']

      #print ("""[DEBUG][FXT] %s""" % _t )

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

      _bb_type = utils.get_ardor_transaction_description(_type, _subtype)

      _from = _t['senderRS']
      _fromurl = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( _from, _from ) 

      if 'recipientRS' in _t:
        _to = _t['recipientRS']
        _tourl = """<a href='/explorer/%s' target=_blank>%s</a> """ % ( _to, _to ) 
      else:
        _to = "Genesis Account"
        _tourl = _to

      _amount = utils.nqt2ardr ( _t['amountNQT'] )
      _b_amount = utils.beauty_float ( _amount ) 

      _fee = utils.nqt2ardr ( _t['feeNQT'] )

      _confirmations = _t['confirmations']
      _confirmations_b = utils.beauty_int(_confirmations)

      _deadline = _t['deadline']
      _date = utils.timestamp2ardortime( _t['timestamp'] )

      _block = _t['block']
      _blockurl = """<a href='/explorer/ablock-%s' target=_blank>%s</a> """ % ( _block, _block ) 

      _fullHash = _t['fullHash']
      _fullHashUrl = """<a href='/explorer/ARDR-%s' target=_blank>%s</a> """ % ( _fullHash, _fullHash )

      _fxt = _t['transaction']
      _fxt_show = """<a href='/explorer/fxt-%s' target=_blank>%s</a> """ % ( _fxt, _fxt )

      page = u"""
  <div class="nb container">
    <div class="nb row">
      <div class="nb col-xs-12 col-sm-12 col-md-12">
        <h4>{{Basic transaction details}}</h4>
        <table class="nb table table-striped">
          <tr><td>{{Type}}</td><td>%s</td></tr> 
          <tr><td>{{From}}</td><td>%s</td></tr> 
          <tr><td>{{To}}</td><td>%s</td></tr> 
          <tr><td>{{Amount}}</td><td>%s ARDR</td></tr> 
          <tr><td>{{Fee}}</td><td>%s ARDR</td></tr> 
          <tr><td>{{Confirmations}}</td><td>%s</td></tr> 
          <tr><td>{{Deadline}}</td><td>%s</td></tr> 
          <tr><td>{{Date}}</td><td>%s UTC</td></tr> 
          <tr><td>{{Parent Tx}}</td><td>%s</td></tr>
          <tr><td>{{Full hash}}</td><td>%s</td></tr>
          <tr><td>{{Block}}</td><td>%s</td></tr> 
        </table>
      </div>
    </div>
  </div>
      """ % (_bb_type, _fromurl, _tourl, _b_amount, _fee, _confirmations_b, _deadline, _date, _fxt_show, _fullHashUrl, _blockurl)

      ########### if we have child chain transactions we need to show it
      if 'attachment' in _t:
        att = _t['attachment']

        if 'chain' in att :
          # have some child chain transactions
          chain = att['chain']
          _b_chain = utils.get_chain_name(chain)

          if 'childTransactionFullHashes' in att:
            # we have children
            p2_header = u"""
        <div class="nb container">
          <div class="nb row">
            <div class="nb col-xs-12 col-sm-12 col-md-12">
              <h4>{{Included transactions in %s chain}}</h4>
              <table class="nb table table-striped">
            """ % ( _b_chain )

            p2_footer = u"""
              </table>
            </div>
          </div>
        </div>
            """ 

            child_list = att['childTransactionFullHashes']

            p2_content = u""

            for i in child_list:
              _child_chain_url = """<a href='/explorer/%s-%s' target=_blank>%s</a> """ % ( _b_chain, i, i )
              p2_content = p2_content + u"""<tr><td>%s</td></tr>""" % ( _child_chain_url )
              
            page2 = p2_header +  p2_content + p2_footer

        else :
          page2 = u"""
          <div class="nb container">
            <div class="nb row">
              <div class="nb col-xs-12 col-sm-12 col-md-12">
                <h4>{{No transactions included}}</h4>
              </div>
            </div>
          </div>
              """ 

      page3 = page + page2

    if 'error' in ttx:
      page3 = u"""%s""" % ttx['error']

    page4 = _(page3, lang)

    result = { 
      'error' : None,
      'data'  : page4
    }
    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200


    return True


  ###############################################################################################################################################################################################
  ###############################################################################################################################################################################################

