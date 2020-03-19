from ibapi.contract import Contract
from liqloopibapi.liqloopibapi import ibapihandle
from liqloopibapi.datatype import *
from threading import Timer
import time
import os


def debug(text):
	print('[MGR] {}'.format(text))

def shutdown():
	print("[MGR] shuting down...")
	os._exit(1)


def main():
	### DEVELOPMENT ONLY
	Timer(10, shutdown).start()

	while True:
		debug("connecting to Gateway and Database...")
		myApi = ibapihandle(gwcnx(), sqlcnx())

		if myApi.isConnected() == True and myApi.database.isConnected() == True :
			debug('Gateway and Database are connected.')

			run = Timer(0, myApi.run).start()
			myApi.initDb()

			# define your search and download
			contract = Contract()
			contract.symbol = 'AAPL'
			#contract.secType = 'OPT'
			#contract.exchange = 'SMART'
			#contract.currency = 'USD'
			#contract.right = 'P'
			#contract.strike = 200
			contract.lastTradeDateOrContractMonth = '20200320'
			myApi.downloadOptionChain(contract)
			shutdown()

		# wait to re create object
		time.sleep(10)

if __name__ == "__main__":
	main()
