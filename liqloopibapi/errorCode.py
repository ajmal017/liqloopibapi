
class errContract():
	def __init__(self):
		self.missing_conId = [1000,'In contract <conId> attribute is missing']
		self.missing_symbol = [1001,'In contract <symbol> attribute is missing']
		self.missing_secType = [1002,'In contract <secType> attribute is missing']
		self.missing_lastTradeDateOrContractMonth = [1003,'In contract <lastTradeDateOrContractMonth> attribute is missing']
		self.missing_strike = [1004,'In contract <strike> attribute is missing']
		self.missing_right = [1005,'In contract <right> attribute is missing']
		self.missing_multiplier = [1006,'In contract <multiplier> attribute is missing']
		self.missing_exchange = [1007,'In contract <exchange> attribute is missing']
		self.missing_primaryExchange = [1008,'In contract <primaryExchange> attribute is missing']
		self.missing_currency = [1009,'In contract <currency> attribute is missing']
		self.missing_localSymbol = [1010,'In contract <localSymbol> attribute is missing']
		self.missing_tradingClass = [1011,'In contract <tradingClass> attribute is missing']
		self.missing_includeExpired = [1012,'In contract <includeExpired> attribute is missing']

		self.invalid_exchange = [1013,'In contract <exchange> attribute is invalid']
		self.warning_exchangeChangeToCBOE = [1014, 'In contract <exchange> attribute will be changed to CBOE']
