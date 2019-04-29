# -*- coding: UTF-8 -*-
#
# API v1 -> ALERT SERVICE
# API v2 -> Blockchain Explorer for Ardor and Nxt
# API v3 -> Asset Explorer for Nxt

import falcon
from inc.model                import *

from route.health             import getHealth
from route.wallet_assets      import getWalletAssets
from route.wallet_currencies  import getWalletCurrencies
from route.wallet_json        import getWalletJSON
from route.wallet_json        import postWalletJSON
from route.wallet_sendmoney   import postWalletSendMoney


class CORS:
  def process_request(self, req, resp):
    resp.set_header( 'Access-Control-Allow-Origin', '*' )

class PeeweeConnect(object):
  def process_request(self, req, resp):
    try :
      sqlite_db.connect()
      #print ("""[%s][DEBUG][BEFORE] open db""" % ( datetime.now() ) )
    except Exception as e:
      print ("""[%s][DEBUG][BEFORE] before request. Exception while connect to DB. [%s].""" % ( datetime.now(), e ) )

  def process_response(self, req, resp, resource):
    if not sqlite_db.is_closed() :
      #print ("""[%s][DEBUG][BEFORE] close db""" % ( datetime.now() ) )
      sqlite_db.close()

app = falcon.API( middleware = [ CORS(), PeeweeConnect() ] )

app.add_route("/api/wallet/health", getHealth() )
app.add_route("/api/wallet/assets/{account}", getWalletAssets() )
app.add_route("/api/wallet/currencies/{account}", getWalletCurrencies() )
app.add_route("/api/wallet/json/{url}", getWalletJSON() )
app.add_route("/api/wallet/savejson", postWalletJSON() )
app.add_route("/api/wallet/sendmoney", postWalletSendMoney())

