# -*- coding: UTF-8 -*-
from datetime             import datetime
from peewee               import *
from os                   import environ
from playhouse.sqlite_ext import *
#from playhouse.pool import PooledPostgresqlExtDatabase

import sys


sqlite_db = SqliteExtDatabase( './database/sigbro_wallet.db', 
                        regexp_function=True, 
                        timeout=3,
                        pragmas={ 
                          ('journal_mode', 'wal'),
                          ('cache_size', -1024 * 4) #4Mb cache
                        }
                      )
sqlite_db.close()

class BaseModel(Model):
  class Meta:
      database = sqlite_db


class WalletJSON(BaseModel):
  timestamp   = TimestampField()
  unsignedTX  = TextField()
  url         = CharField(unique=True)


def init_db():
  sqlite_db.connect()
  sqlite_db.create_tables([WalletJSON])
  sqlite_db.close()
