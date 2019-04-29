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

class ardor_show_something:
  def on_get(self, req, resp, something, lang='en'):
    print ("""[%s][%s] %s""" % ( time.strftime("%Y-%m-%d %H:%M:%S"), self.__class__.__name__, req) )
    ardor = Ardor()

