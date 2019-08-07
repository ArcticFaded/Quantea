# Quantea - A Machine Learning Trader


 This project contains the Quantea framework. Quantea is meant to support Machine Learning based Trading through a standard interface like Sklearn models and allow for ease of backtesting.
 This project is linked with a Frontend React APP: <link to be added>
 
 Information of how to install this app and run it locally can be found below, with information of how to contribute coming soon!


 ## Table of Contents	## Table of Contents


 * [Installing](#install)	
 * [Setting Up Quanty](#setting-up-quanty)
  * [Dependencies](#dependencies)	  * [Dependencies](#dependencies)
  * [Installation](#installation)	    * [Installation](#installation)
* [Writing and Running Tests](#writing-and-running-tests)	    * [Backtesting ML trader](#backtesting-ml-trader)
* [Environment Variables](#environment-variables)	    * [IEX API key](#iex-api-key)
  * [Configuring Packager IP Address](#configuring-packager-ip-address)	  * [User Roles](#user-roles)
  
  
 EXAMPLE USAGE:
```
from marketsim.historic_back_trader import HistoricBackTrader
from technical_indicators.standard_indicators import BollingerBand, EMA
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from actions.get_stock_data import get_historical_prices


start = datetime(2014, 1, 1)
end = datetime.now()

tokens = ['AAPL', 'NVDA']

x = get_historical_prices(start=start, end=end, stocks=tokens, token='enter_token_here')

clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)

trader = HistoricBackTrader(clf, stocks_df=x.AAPL)

trader.add_feature(BollingerBand(N_day=20))
trader.add_feature(EMA(N_day=5))
```
