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
  def on_get(self, req, resp, tx, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    nxt = Nxt()

