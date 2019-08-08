import numpy as np
import pandas as pd

def sim_market(market_actions, market_states, stock):
    actionable_trades = market_actions.predict(market_states[market_states.columns[:-1]])
    return sim_market_results(actionable_trades, market_states, stock)
    

def sim_market_results(actionable_trades, market_states, stock):
    day_of_trades = market_states.index
    type_of_trades = actionable_trades * 1000

    trades = pd.DataFrame(type_of_trades, index=day_of_trades, columns=[stock])
    
    return trades