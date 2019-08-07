import pandas as pd
from .portvals import compute_portvals
from .market_validator import sim_market
from technical_indicators.standard_indicators import BaseTechnicalIndicator
import datetime

class HistoricBackTrader:
    def avg_daily_returns(self, prices):
        return prices / prices.shift(1) - 1
    def cal_portfolio_value(self, port_value):
        return (port_value[-1] / port_value[0]) - 1
    
    def __init__(self, 
                 learner, 
                 stocks_df, 
                 lookback_window=0, 
                 epochs=1, 
                 test_train_split=0.5, 
                 test_train_func=None, 
                 stopping_condition=None):
        """
        An interface to simulate the market in buying and selling
        
        Lookback window refers to the amount of trading days which should be observed prior to starting for TA
        
        test_train_func - custom splitting function
        """
        self.learner=learner
        self.lookback_window=lookback_window
        self.stocks_df = stocks_df
        self.test_train_split = test_train_split
        self.epochs = epochs
        self.stopping_condition = stopping_condition
        self.features = None
        self.discrete = None
        
        
    def add_feature(self, TA, name=None):
        """
        TA is a function which computes a signal based on (for now) closing and volume data
        """
        if (self.discrete is not None):
            raise ValueError("Cannot add more features once discretizer has been added")
        if (self.features is None):
            self.features = pd.DataFrame(index=self.stocks_df.index)
        if (TA.lookback_window > self.lookback_window):
            self.lookback_window = TA.lookback_window
        if (not isinstance(TA, BaseTechnicalIndicator)):
            raise ValueError("TA must inherit BaseTechnicalIndicator")
            
        feature_name = name if name != None else 'X' + str(len(self.features.columns))
        self.features[feature_name] = TA.to_column(self.stocks_df.close)
        return self
    
    def add_discritizer(self, discrete):
        """
        discrete: an array of signals at any timestep t
        """
        if (self.features == None):
            raise ValueError("Must have features to discretize")
        self.discrete = discrete
        return self
        
        
    def train(self, commission=0.00, market_impact=0.000):
        """
        Simulates the market and returns the portfolio with purchases
        """
        if (self.features is None):
            raise ValueError("Trader must have features")
            
        if (self.discrete is None):
            raise ValueError("Trader must implement state representation")
        
        start_date = self.stocks_df.index[0]
        adjusted_start_time = start_date + datetime.timedelta(days=self.lookback_window)
        end_date = self.stocks_df.index[int(len(self.stocks_df) * self.test_train_split)]
        
        market = self.stocks_df.loc[adjusted_start_time:end_date]
        signals = self.features.loc[adjusted_start_time:end_date]
        for epoch in range(self.epoch):
            states = self.discrete(signals)
            actions = self.learner.train(pd.concat[market, states]) # combine close, volume, and signals

            results = sim_market(actions)
            optimum = compute_portvals(market, results, commission=commission, impact=market_impact)
            optimum = optimum / optimum[0]
            optimum_dr = self.avg_daily_returns(optimum)[1:]
            
            if self.verbose:
                print ("Strategic-Based Stats: -----")
                print ('Cumulative Return:', self.cal_portfolio_value(optimum))
                print ('StdDev on Daily Returns:', optimum_dr.std())
                print ('Mean on Daily Returns:', optimum_dr.mean())
            
            if self.stopping_condition and self.stopping_condition(self.cal_portfolio_value(optimum)):
                break
        return results
        
    
    def test(self, commission=0.00, market_impact=0.000):
        """
        Returns how well it performs against the trading window
        """
        start_date = self.stocks_df.index[int(len(self.stocks_df) * self.test_train_split) + 1]
        end_date = self.stocks_df.index[-1]
        
        market = self.stocks_df.loc[start_date:end_date]
        signals = self.features.loc[start_date:end_date]
        
        states = self.discrete(signals)
        actions = self.learner.predict(pd.concat[market, states]) # combine close, volume, and signals
        
        results = sim_market(actions)
        optimum = compute_portvals(market, results, commission=commission, impact=market_impact)
        optimum = optimum / optimum[0]
        optimum_dr = self.avg_daily_returns(optimum)[1:]

        if self.verbose:
            print ("Strategic-Based Stats: -----")
            print ('Cumulative Return:', self.cal_portfolio_value(optimum))
            print ('StdDev on Daily Returns:', optimum_dr.std())
            print ('Mean on Daily Returns:', optimum_dr.mean())
            
        return results