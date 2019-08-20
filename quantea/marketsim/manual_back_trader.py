import pandas as pd
import numpy as np
from .portvals import compute_portvals
from quantea.technical_indicators.standard_indicators import BaseTechnicalIndicator
import datetime
def run_policy(stock, market, resolver, row_helper):
    df_trades = pd.DataFrame(columns = ['date', stock])
    net = 0
    initial_spread = 1000

    for index, row in market.iterrows():
        action = resolver(market.loc[index])
        if action == 1: # BUY
            if net < 1000:
                df_trades = df_trades.append(
                    row_helper(index, stock, initial_spread)
                , ignore_index=True)
                net += initial_spread
            else:
                df_trades = df_trades.append(
                    row_helper(index, stock, 0)
                , ignore_index=True)
        elif action == -1:
            if  net > -1000:
                df_trades = df_trades.append(
                    row_helper(index, stock, -initial_spread)
                , ignore_index=True)
                net -= initial_spread
            else:
                df_trades = df_trades.append(
                    row_helper(index, stock, 0)
                , ignore_index=True)
        if net != 0:        
            initial_spread = 2000
    df_trades = df_trades.set_index('date').astype('int32')
    return df_trades


class ManualBackTrader:
    def avg_daily_returns(self, prices):
        return prices / prices.shift(1) - 1
    def cal_portfolio_value(self, port_value):
        return (port_value[-1] / port_value[0]) - 1
    
    def __init__(self, 
            stocks_df, 
            train_stock,
            verbose=False, 
            lookback_window=0,
            test_train_split=0.5, 
            test_train_func=None, 
            stopping_condition=None):
        """
        
        """
        self.train_stock = train_stock
        self.verbose = verbose
        self.lookback_window=lookback_window
        self.stocks_df = stocks_df[train_stock]
        self.test_train_split = test_train_split
        self.stopping_condition = stopping_condition
        self.features = None
        self.resolve = None
        self.train_trades = None
        self.test_trades = None

    def row_helper(self, Date, Symbol, spread):
        return pd.Series(
            {'date': Date, Symbol: spread}
        )

    def add_resolver(self, resolve):
        """
        discrete: an array of signals at any timestep t
        """
        if (self.features is None):
            raise ValueError("Must have features to resolve")
        self.resolve = resolve
        return self
        
    def add_feature(self, TA, name=None):
        """
        TA is a function which computes a signal based on (for now) closing and volume data
        """
        if (self.resolve is not None):
            raise ValueError("Features cannot be added after signals are decided")
        if (self.features is None):
            self.features = pd.DataFrame(index=self.stocks_df.index)
        if (TA.lookback_window > self.lookback_window):
            self.lookback_window = TA.lookback_window+10
        if (not isinstance(TA, BaseTechnicalIndicator)):
            raise ValueError("TA must inherit BaseTechnicalIndicator")
            
        feature_name = name if name != None else 'X' + str(len(self.features.columns))
        self.features[feature_name] = TA.to_column(self.stocks_df.close)
        return self
    
    def train_policy(self, commission=0.00, market_impact=0.000):
        """
        Simulates the market and returns the portfolio with purchases
        """
        if (self.features is None):
            raise ValueError("Trader must have features")
            
        if (self.resolve is None):
            raise ValueError("Trader must resolve state and generate a signal")

        start_date = self.stocks_df.index[0]
        adjusted_start_time = start_date + datetime.timedelta(days=self.lookback_window)
        end_date = self.stocks_df.index[int(len(self.stocks_df) * self.test_train_split)]

        market = self.stocks_df.loc[adjusted_start_time:end_date].copy()
        market = market / market.iloc[0]
        signals = self.features.loc[adjusted_start_time:end_date].copy()
        signals = signals/signals.iloc[0]
        market = market.join(signals)

        df_trades = run_policy(self.train_stock, market, self.resolve, self.row_helper)
        
        optimum = compute_portvals(market, df_trades, commission=commission, impact=market_impact)
        optimum = optimum / optimum[0]
        optimum_dr = self.avg_daily_returns(optimum)[1:]
        
        if self.verbose:
            print ("Manual-Based Stats: -----")
            print ('Cumulative Return:', self.cal_portfolio_value(optimum))
            print ('StdDev on Daily Returns:', optimum_dr.std())
            print ('Mean on Daily Returns:', optimum_dr.mean())

        return df_trades

    def test_policy(self, commission=0.00, market_impact=0.000):
        """
        Simulates the market and returns the portfolio with purchases
        """
        if (self.features is None):
            raise ValueError("Trader must have features")
            
        if (self.resolve is None):
            raise ValueError("Trader must resolve state and generate a signal")

        start_date = self.stocks_df.index[int(len(self.stocks_df) * self.test_train_split) + 1]
        end_date = self.stocks_df.index[-1]

        market = self.stocks_df.loc[adjusted_start_time:end_date].copy()
        market = market / market.iloc[0]
        signals = self.features.loc[adjusted_start_time:end_date].copy()
        signals = signals/signals.iloc[0]
        market = market.join(signals)

        df_trades = run_policy(self.train_stock, market, self.resolve, self.row_helper)
        
        optimum = compute_portvals(market, df_trades, commission=commission, impact=market_impact)
        optimum = optimum / optimum[0]
        optimum_dr = self.avg_daily_returns(optimum)[1:]
        
        if self.verbose:
            print ("Manual-Based Stats: -----")
            print ('Cumulative Return:', self.cal_portfolio_value(optimum))
            print ('StdDev on Daily Returns:', optimum_dr.std())
            print ('Mean on Daily Returns:', optimum_dr.mean())

        return df_trades
    
    def get_baseline(self, commission=0.00, market_impact=0.000):
        baseline_trades = pd.DataFrame(columns = ['date', self.train_stock])
        initial_spread = 1000

        start_date = self.stocks_df.index[0]
        end_date = self.stocks_df.index[-1]

        market = self.stocks_df.loc[start_date:end_date]

        baseline_trades = baseline_trades.append(
            self.row_helper(market.index[0], self.train_stock, initial_spread), ignore_index=True
        )

        baseline_trades = baseline_trades.set_index('date').astype('int32')

        optimum = compute_portvals(market, baseline_trades, commission=commission, impact=market_impact)
        optimum = optimum / optimum[0]
        optimum_dr = self.avg_daily_returns(optimum)[1:]
        
        if self.verbose:
            print ("Baseline Stats: -----")
            print ('Cumulative Return:', self.cal_portfolio_value(optimum))
            print ('StdDev on Daily Returns:', optimum_dr.std())
            print ('Mean on Daily Returns:', optimum_dr.mean())

        return baseline_trades