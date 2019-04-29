# -*- coding: UTF-8 -*-

from __init__ import __version__

import routes
import base64

from inc.model import *

def str2base64(s):
  return base64.b64encode(s.encode('utf-8'))

def base642str(b):
  return base64.b64decode(b).decode('utf-8')


init_db()

print ("""[%s][INFO] DB initialization completed.""" % (datetime.now()) )
print ("""[%s][INFO] SIGBRO WALLET API Server started. Version: %s """ % (datetime.now(), __version__) )
print (""" """)

