from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.execution import ExecutionFilter
from liqloopibapi.datatype import *
from liqloopibapi.errorCode import *
#import md5
#from liqloopibapi import updateValues
from sqlhandle import sqlhandle
from datetime import datetime
import threading


class ibapihandle(EWrapper, EClient):
	__debugEN = 1
	__debugEN01 = 0

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
		self.database.tblCreate('CBOE_OPT_WORKFLOW', 'CHAR(32)', force=0)

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

	# downloadOPT
	def downloadOptionChain(self, con :Contract, end='', duration='1 Y', tick='1 min', RTH=1, axis=1):
		contractChain = Contract()
		if con.symbol == '' : return errContract().missing_lastTradeDateOrContractMonth
		if con.secType == '' : return errContract().missing_secType
		if con.exchange.upper() != 'CBOE' :
			self.__debug(errContract().warning_exchangeChangeToCBOE)
			con.exchange = 'CBOE'
		if con.currency == '' : return errContract().missing_currency
		if con.right == '' : return errContract().missing_right
		if con.multiplier == '' : return errContract().missing_multiplier

		contractChain.symbol = con.symbol.upper()
		contractChain.secType = con.secType.upper()
		contractChain.exchange = con.exchange.upper()
		contractChain.currency = con.currency.upper()
		contractChain.right = con.right.upper()
		contract.multiplier = con.multiplier

		if axis == 1:
			if con.lastTradeDateOrContractMonth == '' : return errContract().missing_lastTradeDateOrContractMonth
			contractChain.lastTradeDateOrContractMonth = con.lastTradeDateOrContractMonth
		else:
			if con.strike == '' : return errContract().missing_strike
			contractChain.strike = con.strike
