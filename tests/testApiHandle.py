from ibapi.contract import Contract
from liqloopibapi.liqloopibapi import ibapihandle
from liqloopibapi.datatype import *

# create object and init
api = ibapihandle(gwcnx(), sqlcnx())
api.initDb()


# define your search and download
contract = Contract()
contract.symbol = 'AAPL'
contract.secType = 'OPT'
contract.exchange = 'SMART'
contract.currency = 'USD'
contract.right = 'P'
contract.strike = 200
#contract.lastTradeDateOrContractMonth = '20200320'

api.downloadOptionChain(contract)
