from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails
from ibapi.execution import ExecutionFilter
from ibapi.common import BarData
from liqloopibapi.datatype import *
from liqloopibapi.errorCode import *
from sqlhandle import sqlhandle
from threading import Event
from threading import Lock
import copy
import pandas as pd
import numpy as np
from time import sleep
import sys
#from datetime import datetime
#import md5
#import threading


class ibapihandle(EWrapper, EClient):
	debugibapihandle = 1
	debugibapihandle01 = 0
	__reqId = []
	__events = pd.DataFrame([], columns=['reqId', 'funcPnt', 'data'])

	# Debug method
	def __debug(self, *str):
		if self.debugibapihandle == 1 :
			print("[API] {}".format(str))
	def __debug01(self, *str):
		if self.debugibapihandle01 == 1 :
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
		req = self.__events[self.__events['reqId'] == reqId]
		if len(req) != 0 :
			row = req.index.values.astype(int)[0]
			if self.__events.at[row, 'funcPnt'] != None : self.__events.at[row, 'funcPnt'].set()
		self.__debug("reqId={} errorCode=<{}>".format(reqId, errorCode), errorString)

	def connectApi(self):
		self.__debug('connecting to API gateway', self.__gwcnx)
		self.connect(self.__gwcnx.host, self.__gwcnx.port, self.__gwcnx.clientId)

	def connectDb(self):
		self.__debug('connecting to SQL database', self.__sqlcnx)
		self.database = sqlhandle(self.__sqlcnx.host, self.__sqlcnx.user, self.__sqlcnx.password)
		self.database.debugibapihandle = 1

	def initDb(self):
		# init base structure # init mktData db
		c = contractArray()
		self.database.dbCreate('history')
		self.database.dbCreate('live')
		#self.database.tblCreate('CBOE_OPT_WORKFLOW', 'CHAR(32)', force=0)

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
		req = self.__events[self.__events['reqId'] == reqId]
		if len(req) != 0 :
			row = req.index.values.astype(int)[0]
			self.__events.drop([row], axis=0, inplace=True)

	# GET Methods
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

	def getHistoricalBarData(self, contract :Contract, end, duration, tick, type, timeout=60):
		self.__debug(contract.conId, end, duration, tick, type, timeout)
		getHistoricalData_event = Event()
		getHistoricalData_data = []
		reqId = self.getReqId()

		self.__events = self.__events.append(pd.DataFrame([[reqId, getHistoricalData_event, getHistoricalData_data]], columns=self.__events.columns), ignore_index=True)
		self.reqHistoricalData(reqId, contract, end, duration, tick, type, 1, 1, False, [])
		getHistoricalData_event.wait(timeout)

		try:
			if len(getHistoricalData_data) > 0:
				if isinstance(getHistoricalData_data[0], BarData) :
					res = getHistoricalData_data
					self.__debug('getHistoricalData <{}> Block <{}> Items <{}>'.format(contract.conId, end, len(getHistoricalData_data)))
				else:
					res = 1
					self.__debug("getHistoricalData <{}> <Invalid data>".format(contract.conId))
			else:
				res = 2
				self.__debug('getHistoricalData <{}> <No data received>'.format(contract.conId))
		finally:
			self.rmReqId(reqId)
			return res

	def downloadOptionChain(self, con :Contract):
		downloadOptionChain_event = Event()
		downloadOptionChain_data = []

		contractUL = Contract()
		contractUL.symbol = con.symbol.upper()
		contractUL.secType = 'STK'
		contractUL.exchange = 'SMART'
		contractUL.currency = 'USD'

		# get conId form underlaying
		res = self.getContractDetails(contractUL)
		if type(res) == list :
			contractUL = res[0].contract
		else:
			return res

		axis =1
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
			optionChain = []
			res = self.getContractDetails(contractChain, event=0,timeout=5)
			if type(res) == list :
				for item in res:
					optionChain.append(item.contract)
			else:
				return res

			# add optionChain contracts to table general.contract
			self.tblContractAppend(optionChain)

			# add IF not EXISTs in general.optionChain
			#self.tblOptionChainAppend(contractUL)
			# add to contract_optionChain
			#self.tblContractOptionChainAppend(contractChain, optionChain)

		else:
			return 'Dev. Stage'
			#if con.strike == '' : return errContract().missing_strike
			#contractChain.strike = con.strike

	# TABLE APPREND METHODs
	# DEF tblHistoricalBarDataAppend
	def tblHistoricalBarDataAppend(self, contract :Contract, barDataList, dry=0):
		barDataArr = barDataArray()
		table = 'history.{}'.format(contract.conId)
		for item in barDataList:
			barDataArr.df = barDataArr.df.append(pd.DataFrame([[	item.open, item.high, item.low, item.close, item.volume, item.average, item.barCount
										]], [pd.to_datetime(item.date)], barDataArr.df.columns))
		if dry == 0:
			self.database.tblCreateFromDataFrame(table, barDataArr.df, barDataArr.sqlhead[1], indexname='date', data=0)
			self.database.tblInsertDataFrame(table, barDataArr.df, indexname='date', insert='INSERT IGNORE INTO')
		return barDataArr
	# END tblHistoricalBarDataAppend
	# DEF tblContractAppend
	def tblContractAppend(self, contractList):
		df = contractArray().df
		for item in contractList:
			df = df.append(pd.DataFrame([[	item.symbol, item.secType, item.lastTradeDateOrContractMonth,
											item.strike, item.right, item.multiplier, item.exchange, item.primaryExchange,
											item.currency, item.localSymbol, item.tradingClass, int(item.includeExpired), item.secType
										]], [item.conId], df.columns))
		return self.database.tblInsertDataFrame('general.contract', df, indexname='conId', insert='INSERT IGNORE INTO')
	# END tblContractAppend
	# ignore
	def tblOptionChainAppend(self, contract :Contract):
		arr = [	['conId', 'symbol', 'secType', 'currency', 'tblOptionName'],
				[contract.conId, contract.symbol, contract.secType, contract.currency, '{}_OPT'.format(contract.symbol)]]
		return self.database.tblInsertArray('general.optionChain', arr, insert='INSERT IGNORE INTO')
	# ignore
	def tblContractOptionChainAppend(self, contract :Contract, contractList):
		# create table, if needed
		table = 'general.{}_optionChain_Put'.format(contract.symbol)
		date = 'conId_{}'.format(contract.lastTradeDateOrContractMonth)
		if type(self.database.tblCreate(table, 'strike FLOAT NOT NULL', 'conRight VARCHAR(255) NOT NULL', '{} INT UNIQUE'.format(date))) != int:
			self.database.tblAlter(table, 'ADD {} INT UNIQUE'.format(date))

		df = pd.DataFrame([], columns=['strike', 'conRight', date])
		for item in contractList:
			df = df.append(pd.DataFrame([[item.strike, item.right, item.conId]], columns=df.columns), ignore_index=True)
		#print(df)
		self.database.tblInsertDataFrame(table, df, insert='INSERT IGNORE INTO', incl_index=0)
		# make DataFrame and INSERT
		# no error, and right execution, however, not working
		# if you copy the string code and execute it in the console, it works...
		#for item in df[df['right'] == 'P'].index :
			#self.database.execute('INSERT INTO {table} (strike, {date}) VALUES ({strike}, {conId}) ON DUPLICATE KEY UPDATE {date}={conId}'.format(table=tablePut, date=date, strike=df.loc[item, 'strike'], conId=df.loc[item, date]))


	# CALL BACK METHODs
	# contractDetails
	def contractDetails(self, reqId :int, contractDetails :Contract):
		req = self.__events[self.__events['reqId'] == reqId]
		if len(req) != 0 :
			row = req.index.values.astype(int)[0]
			self.__events.at[row, 'data'].append(contractDetails)
			if self.__events.at[row, 'funcPnt'] != None : self.__events.at[row, 'funcPnt'].set()
	# END contractDetails
	# DEF historicalData
	def historicalData(self, reqId :int, bar :BarData):
		#print('histData')
		try:
			req = self.__events[self.__events['reqId'] == reqId]
			if len(req) != 0 :
				row = req.index.values.astype(int)[0]
				self.__events.at[row, 'data'].append(bar)
				#print('apprended', len(self.__events.at[row, 'data']))
		except:
			print('[ERROR] historicalData(reqId={}, bar={}), req={}, row={}'.format(reqId, bar, req, row))
	# END historicalData
	# DEF historicalDataEnd
	def historicalDataEnd(self, reqId :int, start :str, end :str):
		#print('histDataEnd')
		super().historicalDataEnd(reqId, start, end)
		req = self.__events[self.__events['reqId'] == reqId]
		if len(req) != 0 :
			row = req.index.values.astype(int)[0]
			if self.__events.at[row, 'funcPnt'] != None : self.__events.at[row, 'funcPnt'].set()
	# END historicalDataEnd
