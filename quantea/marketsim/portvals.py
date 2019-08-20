import pandas as pd
import numpy as np

def compute_portvals(market, orders, commission=0.00, impact=0.000, start_val=100000):
    """
    market : Market_DataFrame returned by actions.get_stock_data
    orders : Dataframe of format
        {
            'date': trading day,
            <TICKER>: <ORDER>
        }

    orders should be indexed by the 'date' column.

    where ticker is the stock ticker, and order is the amount to buy (+ number), sell (- number), short (if net orders is negative), and hold (if order is 0)
    holding does not need to be specified however.
    """
    orders.sort_index(inplace=True)
    orders = orders.loc[orders.index.isin(market.index)]
    symbols = orders.columns
    trades = pd.DataFrame(index=market.index, 
                          data=np.zeros((len(market), len(symbols) + 1)), 
                          columns=symbols.tolist() + ['CASH'])
    
    order_on_days = market.loc[orders.index.unique()]
    market.loc[:,'CASH'] = np.ones(len(market))

    # this function can be vectorized, LOOKING into it
    for index, row in order_on_days.iterrows():
        # each row is a trading day
        execute = orders[orders.index == index]
        for _, diff in execute.iterrows():
            traded_symbols = diff[~np.isnan(diff)].index # get all stocks which traded on this day
            for stock in traded_symbols:
                trades.loc[index, stock] +=  diff[stock]
                impact_on_trade = (1 + impact) if diff[stock] > 0 else (1 - impact)
                current_cash = trades.loc[index, 'CASH']
                if len(symbols) == 1:
                    trades.loc[index, 'CASH'] = current_cash + (row['close'] * -diff[stock] * impact_on_trade) - (commission)
                else:
                    trades.loc[index, 'CASH'] = current_cash + (row[(stock, 'close')] * -diff[stock] * impact_on_trade) - (commission)
    holdings = trades.cumsum()
    holdings.loc[:, 'CASH'] += start_val
    if len(symbols) == 1:
        market = market.drop(columns=['volume'])
        market = market.rename(columns={'close': symbols[0]})


        value =  holdings * market
    else:
        closing = market[ [(x, 'close')  for x in market.columns.levels[0] ] ].stack()
        closing.index = closing.index.droplevel(1)
        value =  holdings * closing[ [x for x in holdings.columns[:-1]] ]
    
    return value.sum(axis=1)