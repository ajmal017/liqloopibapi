from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails
from ibapi.execution import ExecutionFilter
from liqloopibapi.datatype import *
from liqloopibapi.errorCode import *
from sqlhandle import sqlhandle
from threading import Event
from threading import Lock
import copy
import pandas as pd
import numpy as np
from time import sleep
#from datetime import datetime
#import md5
#import threading


class ibapihandle(EWrapper, EClient):
	__debugEN = 1
	__debugEN01 = 0
	__reqId = []
	__events = pd.DataFrame([], columns=['reqId', 'funcPnt', 'data'])

	# Debug method
	def __debug(self, *str):
		if self.__debugEN == 1 :
			print("[API] {}".format(str))
	def __debug01(self, *str):
		if self.__debugEN01 == 1 :
			print("[API] {}".format(str))

	# init
	def __init__(self, gwconnection :gwcnx, sqlconnection :sqlcnx):
		self.__debug("initializing...")
		EClient.__init__(self, self)
		self.nextOrderId = 0
		self.__gwcnx = gwconnection
		self.__sqlcnx = sqlconnection
		self.database = None
		self.connectApi()
		self.connectDb()

	def get_gwcnx(self):
		return self.__gwcnx
	def get_sqlcnx(self):
		return self.__sqlcnx

	def error(self, reqId, errorCode, errorString):
		self.__debug("<{}>".format(errorCode), errorString)

	def connectApi(self):
		self.__debug('connecting to API gateway', self.__gwcnx)
		self.connect(self.__gwcnx.host, self.__gwcnx.port, self.__gwcnx.clientId)

	def connectDb(self):
		self.__debug('connecting to SQL database', self.__sqlcnx)
		self.database = sqlhandle(self.__sqlcnx.host, self.__sqlcnx.user, self.__sqlcnx.password)
		self.database.setDebug(level=1, value=0)

	def initDb(self):
		# init base structure # init mktData db
		c = contractArray()
		self.database.dbCreate('history')
		self.database.tblCreateFromArray('history.contract', c.sqlhead, data=0)
		#self.database.tblCreate('CBOE_OPT_WORKFLOW', 'CHAR(32)', force=0)

		self.database.dbCreate('live')
		self.database.tblCreateFromArray('live.contract', c.sqlhead, data=0)

		self.database.dbCreate('general')
		self.database.tblCreateFromArray('general.contract', c.sqlhead, data=0)
		self.database.tblCreate('general.optionChain', c.conId.keystr, c.symbol.keystr, c.secType.keystr, c.currency.keystr, 'tblOptionName VARCHAR(255)', force=0)

		# init Account structure
		if self.__gwcnx.account != '':
			self.database.dbAvailable('IBAccount', force=1)
			# Account Table
			#self.myDatabase.tblCreateFromArrayH(self.__accountID, accountArray)
			#self.myDatabase.tblInsert(self.__accountID, "tag, value", "'created', '{}'".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			# Filter Tables
			#self.myDatabase.tblCreateFromArrayH("{}FilterAccountMin".format(self.__accountID), filterArray)
			#self.myDatabase.tblCreateFromArrayH("{}FilterExecution".format(self.__accountID), filterArray)
			#self.myDatabase.tblCreateFromArrayH("{}FilterOpenPosition".format(self.__accountID), filterArray)
			# Update Tables
			#self.myDatabase.tblCreateFromArrayH("{}updateExecution".format(self.__accountID), updateExecutionArray)
			#self.myDatabase.tblCreateFromArrayH("{}updateAccount".format(self.__accountID), updateAccountArray)
			#self.myDatabase.tblCreateFromArrayH("{}updatePosition".format(self.__accountID), updatePositionArray)
			#self.myDatabase.tblCreateFromArrayH("{}updateOpenOrder".format(self.__accountID), updateOpenOrderArray)

	def getReqId(self):
		new = np.random.randint(np.random.randint(2147483647))
		while new in self.__reqId:
			new = np.random.randint(np.random.randint(2147483647))
		self.__reqId.append(int(new))
		return int(new)

	def rmReqId(self, reqId):
		self.__reqId.remove(reqId)

	def getContractDetails(self, contract :Contract, timeout=2, event=1):
		getConId_event = None
		getConId_data = []
		reqId = self.getReqId()
		if event == 1: getConId_event = Event()

		self.__events = self.__events.append(pd.DataFrame([[reqId, getConId_event, getConId_data]], columns=self.__events.columns), ignore_index=True)
		self.reqContractDetails(reqId, contract)
		if event == 1: getConId_event.wait(timeout)
		else:
			sleep(timeout)
			# delete event
		try:
			if len(getConId_data) > 0:
				if type(getConId_data[0]) == ContractDetails :
					res = getConId_data
					self.__debug('getContractDetails <{}> {}'.format(contract.symbol, len(getConId_data)))
				else:
					res = 1
					self.__debug("getConId_data <Invalid data>")
			else:
				res = 2
				self.__debug('getConId_data <No data received>')
		finally:
			self.rmReqId(reqId)
			return res

	def downloadOptionChain(self, con :Contract, end='', duration='1 Y', tick='1 min', RTH=1, axis=1):
		downloadOptionChain_event = Event()
		downloadOptionChain_data = []

		contractUL = Contract()
		contractUL.symbol = con.symbol.upper()
		contractUL.secType = 'STK'
		contractUL.exchange = 'SMART'
		contractUL.currency = 'USD'

		# get conId form underlaying
		self.__debug(self.getContractDetails(contractUL)[0].contract.conId)

		contract = Contract()
		contract.symbol = 'AAPL'
		contract.secType = 'OPT'
		contract.exchange = 'CBOE'
		contract.lastTradeDateOrContractMonth = '20200320'
		contract.multiplier = 100


		print('---')
		res = self.getContractDetails(contract, timeout=2, event=0)
		print(len(res))
		for item in res:
			print(item.contract.conId, item.contract.symbol, item.contract.right, item.contract.strike)

		return 1
		if axis == 1:
			# init input data
			contractChain = Contract()
			if con.lastTradeDateOrContractMonth == '' : return errContract().missing_lastTradeDateOrContractMonth
			if con.symbol == '' : return errContract().missing_symbol
			if con.secType == '' :
				errContract().warning_secTypeToOPT
				con.secType = 'OPT'
			if con.exchange.upper() != 'CBOE' :
				errContract().warning_exchangeChangeToCBOE
				con.exchange = 'CBOE'
			if con.currency == '' :
				errContract().warning_currencyChangeToUSD
				con.currency = 'USD'
			if con.multiplier == '' :
				errContract().warning_multiplierChangeTo100
				con.multiplier == 100
			contractChain.symbol = con.symbol.upper()
			contractChain.secType = con.secType.upper()
			contractChain.exchange = con.exchange.upper()
			contractChain.currency = con.currency.upper()
			contractChain.right = con.right.upper()
			contractChain.multiplier = con.multiplier
			contractChain.lastTradeDateOrContractMonth = con.lastTradeDateOrContractMonth

			# download optionChain
			print('ok')
			self.__events = self.__events.append(pd.DataFrame([[self.nextOrderId, None, downloadOptionChain_data]], columns=self.__events.columns), ignore_index=True)


		else:
			return 'Dev. Stage'
			#if con.strike == '' : return errContract().missing_strike
			#contractChain.strike = con.strike

	# contractDetails
	def contractDetails(self, reqId :int, contractDetails :Contract):
		req = self.__events[self.__events['reqId'] == reqId]
		if len(req) != 0 :
			row = req.index.values.astype(int)[0]
			self.__events.at[row, 'data'].append(copy.deepcopy(contractDetails))
			if self.__events.at[row, 'funcPnt'] != None :
				self.__events.at[row, 'funcPnt'].set()
				self.__events.drop([row], axis=0, inplace=True)
	# END contractDetails
