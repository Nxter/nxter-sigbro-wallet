# -*- coding: UTF-8 -*-

import json
import datetime
import time

from __init__ import __version__

class getHealth:
  def on_get(self, req, resp):
    res = { 'application':'SIGBRO WALLET API', 'version' : __version__, 'health' : 'ok' }
    resp.body = json.dumps(res)
