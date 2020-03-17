from threading import Timer
import os
import threading
import time



class manager():
	def __init__():

	def run():
		### DEVELOPMENT ONLY
		Timer(10, shutdown).start()

		while True:
			print("[MGR] connecting to Gateway and Database...")
			myApi = ibapihandle(gateway_ip, gateway_port, gateway_clientID, accountID, sql_host, sql_user, sql_pw)

			if myApi.isConnected() == True and myApi.myDatabase.isConnected() == True :
				run = threading.Timer(0, myApi.run).start()
				myApi.initDb()
				while myApi.isConnected() == True and myApi.myDatabase.isConnected() == True :
					myApi.start()
					time.sleep(updateInterval)

			# wait to re create object
			time.sleep(10)
