'''
datatype.py
'''
import numpy as np
import pandas as pd

class contractArray():
	"""
	Array to collect contract(s) information
	"""
	class attr():
		def __init__(self, var):
			self.key = var
			self.name = var[0]
			self.type = var[1]
			self.keystr = ' '.join(var)

	def __init__(self):
		self.sqlkey = [	["conId", "INT NOT NULL UNIQUE PRIMARY KEY"], \
						["symbol", "VARCHAR(255)"], \
						["secType", "VARCHAR(255)"], \
						["lastTradeDateOrContractMonth", "DATETIME"], \
						["strike", "FLOAT"], \
						["conRight", "VARCHAR(255)"], \
						["multiplier", "FLOAT"], \
						["exchange", "VARCHAR(255)"], \
						["primaryExchange", "VARCHAR(255)"], \
						["currency", "VARCHAR(255)"], \
						["localSymbol", "VARCHAR(255)"], \
						["tradingClass", "VARCHAR(255)"], \
						["includeExpired", "INT"], \
						["secIdType", "VARCHAR(255)"] ]
		self.sqlhead = np.transpose(self.sqlkey)

		self.conId = self.attr(self.sqlkey[0])
		self.symbol = self.attr(self.sqlkey[1])
		self.secType = self.attr(self.sqlkey[2])
		self.lastTradeDateOrContractMonth = self.attr(self.sqlkey[3])
		self.strike = self.attr(self.sqlkey[4])
		self.conRight = self.attr(self.sqlkey[5])
		self.multiplier = self.attr(self.sqlkey[6])
		self.exchange = self.attr(self.sqlkey[7])
		self.primaryExchange = self.attr(self.sqlkey[8])
		self.currency = self.attr(self.sqlkey[9])
		self.localSymbol = self.attr(self.sqlkey[10])
		self.tradingClass = self.attr(self.sqlkey[11])
		self.includeExpired = self.attr(self.sqlkey[12])
		self.secIdType = self.attr(self.sqlkey[13])

		self.df = pd.DataFrame([], columns=self.sqlhead[0])
		self.df.set_index('conId', inplace=True)

class sqlcnx():
	"""
	Object for sql Database
	"""
	def __init__(self, host='localhost', port=3306, user='root', password='root'):
		self.host = host
		self.port = port
		self.user = user
		self.password = password

	def __str__(self):
		return ''.join("{}:{}@{}:{}".format(self.user, self.password, self.host, self.port))
	def __repr__(self):
		return ''.join("{}:{}@{}:{}".format(self.user, self.password, self.host, self.port))

class gwcnx():
	"""
	Object for gateway Connection
	"""
	def __init__(self, host='localhost', port=4000, clientId=0, account = ''):
		self.host = host
		self.port = port
		self.clientId = clientId
		self.account = account

	def __str__(self):
		return ''.join("{}({})@{}:{}".format(self.account, self.clientId, self.host, self.port))
	def __repr__(self):
		return ''.join("{}({})@{}:{}".format(self.account, self.clientId, self.host, self.port))
