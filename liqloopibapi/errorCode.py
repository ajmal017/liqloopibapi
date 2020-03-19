
class errContract():
	def showErr(self, var):
		print('[ERROR]', var)

	def showInfo(self, var):
		print('[INFO]', var)

	@property
	def missing_conId(self):
		msg = [1000,'In contract <conId> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_symbol(self):
		msg = [1001,'In contract <symbol> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_secType(self):
		msg = [1002,'In contract <secType> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_lastTradeDateOrContractMonth(self):
		msg = [1003,'In contract <lastTradeDateOrContractMonth> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_strike(self):
		msg = [1004,'In contract <strike> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_right(self):
		msg = [1005,'In contract <right> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_multiplier(self):
		msg = [1006,'In contract <multiplier> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_exchange(self):
		msg = [1007,'In contract <exchange> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_primaryExchange(self):
		msg = [1008,'In contract <primaryExchange> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_currency(self):
		msg = [1009,'In contract <currency> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_localSymbol(self):
		msg = [1010,'In contract <localSymbol> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_tradingClass(self):
		msg = [1011,'In contract <tradingClass> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def missing_includeExpired(self):
		msg = [1012,'In contract <includeExpired> attribute is missing']
		self.showErr(msg)
		return msg

	@property
	def invalid_exchange(self):
		msg = [1013,'In contract <exchange> attribute is invalid']
		self.showErr(msg)
		return msg

	@property
	def warning_exchangeChangeToCBOE(self):
		msg = [1014, 'In contract <exchange> attribute will be changed to CBOE']
		self.showInfo(msg)
		return msg

	@property
	def warning_secTypeToOPT(self):
		msg = [1015, 'In contract <secType> attribute will be changed to OPT']
		self.showInfo(msg)
		return msg

	@property
	def warning_currencyChangeToUSD(self):
		msg = [1016, 'In contract <currency> attribute will be changed to USD']
		self.showInfo(msg)
		return msg

	@property
	def warning_multiplierChangeTo100(self):
		msg = [1017, 'In contract <multiplier> attribute will be changed to 100']
		self.showInfo(msg)
		return msg
