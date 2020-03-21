			if con.lastTradeDateOrContractMonth == '' : return errContract().missing_lastTradeDateOrContractMonth
			if int(con.conId) == int(0) :
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
