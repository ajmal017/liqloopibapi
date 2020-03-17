'''
datatype.py
'''

class sqlcnx():
	def __init__(self, host='localhost', port=3306, user='root', pw='root'):
		self.host = host
		self.port = port
		self.user = user
		self.pw = pw

	def __str__(self):
		return ''.join("{}:{}@{}:{}".format(self.user, self.pw, self.host, self.port))



class gwcnx():
	def __init__(self, host='localhost', port=4000, account = ''):
		self.host = host
		self.port = port
		self.account = account

	def __str__(self):
		return ''.join("{}@{}:{}".format(self.account, self.host, self.port))
