from ibapi.contract import Contract
from liqloopibapi.liqloopibapi import ibapihandle
from liqloopibapi.datatype import *
from threading import Timer
from datetime import datetime
import time
import os


def debug(text):
	print('[MGR] {}'.format(text))

def shutdown():
	print("[MGR] shuting down...")
	os._exit(1)


def main():
	### DEVELOPMENT ONLY
	#Timer(10, shutdown).start()

	while True:
		debug("connecting to Gateway and Database...")
		myApi = ibapihandle(gwcnx(), sqlcnx(host='liqloop.breath2live.de', password='299792458'))
		myApi.database.debugEN = 0

		if myApi.isConnected() == True and myApi.database.isConnected() == True :
			debug('Gateway and Database are connected.')

			run = Timer(0, myApi.run).start()
			myApi.initDb()

			# define your search and download
			contract = Contract()
			contract.symbol = 'ADBE'
			contract.currency = 'USD'
			contract.lastTradeDateOrContractMonth = '20200320'
			myApi.downloadOptionChain(contract)

			dfContract = myApi.database.tblReadToDataFrame('*', 'general.contract', index='conId')
			dfFilter = dfContract[(dfContract['symbol']==contract.symbol) & (dfContract['lastTradeDateOrContractMonth']==contract.lastTradeDateOrContractMonth)]

			print('[Found]', len(dfFilter), 'of', len(dfContract), 'contracts in Database matching Filter settings')

			cnt_all = len(dfFilter.index)
			cnt = 1
			start = datetime.now()
			print(cnt_all, 'Packages to download. Starting at', start)
			errList = []

			myApi.debugEN = 0
			myApi.database.debugEN = 0

			for conId in dfFilter.index:
				histContract = Contract()
				histContract.conId = conId
				histContract.exchange = 'CBOE'

				histBarData = myApi.getHistoricalBarData(histContract, '20200320 00:00:00', '6 M', '1 hour', 'TRADES', timeout=20)
				if type(histBarData) == list: myApi.tblHistoricalBarDataAppend(histContract, histBarData)
				else: errList.append(conId)
				print('[{}]'.format(conId), '{}% |'.format(round(cnt/cnt_all*100, 2)), cnt, 'of', cnt_all , 'Packages requested. Error List: {}.'.format(len(errList)), 'Running:', datetime.now()-start, 'Remaining Time:', (datetime.now()-start)/cnt*(cnt_all-cnt) ) #(cnt_all - cnt)*(datetime.now()-start)/(cnt+1))
				cnt += 1
			end = datetime.now()
			print('All Packages downloaded at', end)
			print('Total time:', end-start)

			print('Packages Lost {lost} out of {max} | {pct}%'.format(lost=len(errList), max=cnt_all, pct=round(len(errList)/cnt_all*100, 2)))
			print('Packages Lost:', errList)

			Timer(0, shutdown).start()


		# wait to re create object
		time.sleep(10)

if __name__ == "__main__":
	main()
