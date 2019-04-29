# -*- coding: UTF-8 -*-

from inc.ardor  import Ardor
from inc.nxt    import Nxt

from inc        import utils
from inc.local  import translate as _

import json
import random
import hashlib
import falcon
import time
import re

class search_something:
  def on_get(self, req, resp, query):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )

    # compile regexp
    nxt   = re.compile(r"""NXT-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{5}""", re.IGNORECASE)
    ardor = re.compile(r"""ARDOR-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{5}""", re.IGNORECASE)
    multi = re.compile(r"""^[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{5}""", re.IGNORECASE)
    tx    = re.compile(r"""[0-9]{18,20}""")

    urls = []


    _nxt   = Nxt()
    _ardor = Ardor()
    
    template = """<ul class='list-group'>"""
    template = template + """<li class='list-group-item'>Nothing found</li>""" 
    template = template + """</ul>"""


    if nxt.search(query) :
      # check Nxt account
      template = """<ul class='list-group'>"""
      t = json.loads(_nxt.get_account_info(query))
      print ("""NXT: %s""" % t)
      if 'data' in t and t['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/%s' target=_blank>%s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp
      else :
        template = template + """<li class='list-group-item'>No Nxt account found</li>""" 

      template = template + """</ul>"""

    if ardor.search(query) :
      # check Ardor account
      template = """<ul class='list-group'>"""
      t = json.loads(_ardor.get_account_exist(query))
      if 'data' in t and t['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/%s' target=_blank>%s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp
      else :
        template = template + """<li class='list-group-item'>No Ardor account found</li>""" 
      template = template + """</ul>"""

    if multi.search(query) :
      template = """<ul class='list-group'>"""
      t1 = json.loads(_nxt.get_account_info("NXT-" + query))
      if 'data' in t1 and t1['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/NXT-%s' target=_blank>NXT-%s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp
      else :
        template = template + """<li class='list-group-item'>No Nxt account found</li>""" 

      t2 = json.loads(_ardor.get_account_exist("ARDOR-" + query))
      if 'data' in t2 and t2['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/ARDOR-%s' target=_blank>ARDOR-%s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp
      else :
        template = template + """<li class='list-group-item'>No Ardor account found</li>""" 
      template = template + """</ul>"""


    if tx.search(query) : 
      # tx, assetid, blockid
      template = """<ul class='list-group'>"""

      t1 = json.loads(_nxt.get_tx_info(query))
      if 'data' in t1 and t1['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/tx-%s' target=_blank>Nxt Transaction %s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp

      t2 = json.loads(_nxt.get_asset_info(query))
      if 'data' in t2 and t2['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/asset-%s' target=_blank>Nxt Asset ID %s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp

      t3 = json.loads(_nxt.get_block_info(query))
      if 'data' in t3 and t3['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/block-%s' target=_blank>Nxt Block ID %s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp

      t4 = json.loads(_ardor.get_fxt_info(query))
      if 'data' in t4 and t4['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/fxt-%s' target=_blank>Ardor Fxt transaction %s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp

      t5 = json.loads(_ardor.get_block_info(query))
      print (t5)
      if 'data' in t5 and t5['data'] != None :
        tmp = """<a href='https://www.nxter.org/explorer/ablock-%s' target=_blank>Ardor Block ID %s</a>""" % (query,query)
        template = template + """<li class='list-group-item'>%s</li>""" % tmp


      template = template + """</ul>"""
#
 #     tmp = """https://www.nxter.org/tx-%s""" % query
 #     urls.append(tmp)
 #     tmp = """https://www.nxter.org/asset-%s""" % query
 #     urls.append(tmp)
 #     tmp = """https://www.nxter.org/block-%s""" % query
 #     urls.append(tmp)
 #     tmp = """https://www.nxter.org/fxt-%s""" % query
 #     urls.append(tmp)
      
      
    result = { 
      'error' : None,
      'data'  : template
    }

    resp.body = json.dumps(result)
    resp.status = falcon.HTTP_200

    return True

