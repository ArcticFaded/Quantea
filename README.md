# Quantea - A Machine Learning Trader


 This project contains the Quantea framework. Quantea is meant to support Machine Learning based Trading through a standard interface like Sklearn models and allow for ease of backtesting.
 This project is linked with a Frontend React APP: <link to be added>
 
 Information of how to install this app and run it locally can be found below, with information of how to contribute coming soon!


 ## Table of Contents	## Table of Contents


 * [Installing](#install)	
 * [Setting Up Quantea](#setting-up-quantea)
  * [Dependencies](#dependencies)
* [Writing and Running Tests](#writing-and-running-tests)
* [Environment Variables](#environment-variables)
  * [Configuring Packager IP Address](#configuring-packager-ip-address)
  
  
 ## Install
 From PyPI with pip (latest stable release):

 ``$ pip3 install quantea``

 From development repository (dev version):

 .. code:: bash

      $ git clone https://github.com/ArcticFaded/Quantea.git
      $ cd quantea
      $ python3 setup.py install
  
 ## Setting Up Quantea
 Quantea relies on MongoDB to cache responses from IEX in order prevent rate limiting API request to IEX cloud while allowing for multiple re-testing sessions.
  
  #### Dependencies
  
  #### MongoDB
  
 EXAMPLE USAGE:
```
from quantea.marketsim.historic_back_trader import HistoricBackTrader
from quantea.technical_indicators.standard_indicators import BollingerBand, EMA, MACD
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from datetime import datetime
from quantea.actions.get_stock_data import get_historical_prices
import numpy as np

start = datetime(2014, 1, 1)
end = datetime.now()

tokens = ['AAPL', 'NVDA']

# example call with fake token (replace with your own)
x = get_historical_prices(start=start, end=end, stocks=tokens, token='your_iex_token_here')

clf = AdaBoostClassifier(n_estimators=2,) #max_depth=2)

trader = HistoricBackTrader(clf, stocks_df=x, train_stock='NVDA', verbose=True)

trader.add_feature(BollingerBand(N_day=26))
trader.add_feature(MACD(N1=26, N2=12))

trader.add_discritizer(lambda x: np.sum(x, axis=1))

tt = trader.train()
testt = trader.test()
```
