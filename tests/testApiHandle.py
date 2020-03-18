from liqloopibapi.liqloopibapi import ibapihandle
from liqloopibapi.datatype import *

api = ibapihandle(gwcnx(), sqlcnx())
api.initDb()
