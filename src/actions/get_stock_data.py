from datetime import datetime
from iexfinance.stocks import get_historical_data
from db.controllers.store_stocks import store_stock_data, store_stocks_data, should_call_api
from db.controllers.get_stocks import get_stock_date_for_period
from db.models import Stock
from typing import List, Dict
import pandas as pd

OUTPUT_FORMAT = enumerate(
    ["pandas"]
)


def get_historical_prices(start: datetime, end: datetime, token: str = None, stocks: List[str] = ["AAPL"], close_only: bool = True, output_format: str = "pandas"):
    """
    First checks if database has information on the stock, if it doesn't it will make a request
    """
    if start is None or end is None:
        raise ValueError("Requires start and end time")

    if len(stocks) == 0:
        raise ValueError("Must provide at least one stock")

    if (not isinstance(stocks, list)):
        raise ValueError("Stocks must be a list")
    
    if len(stocks) == 1 and stocks[0] == 'SPY':
        trades_df = get_historical_data(stocks, start, end, close_only=close_only, output_format=output_format, token=token)
        store_stock_data(trades_df, stocks[0])
        trades_df.columns=pd.MultiIndex.from_tuples([(stocks[0],x) for x in trades_df.columns])
        return trades_df

    if should_call_api(stocks, start, end):
        if token is None:
            raise ValueError("Stock not in database, requires a IEX cloud token")
        trades_df = get_historical_data(stocks, start, end, close_only=close_only, output_format=output_format, token=token)
        
        if len(stocks) == 1:
            store_stock_data(trades_df, stocks[0])
        else:
            store_stocks_data(trades_df, stocks)

        if (len(stocks) == 1):
            trades_df.columns=pd.MultiIndex.from_tuples([(stocks[0],x) for x in trades_df.columns])
        return trades_df
    else:
        return get_stock_date_for_period(stocks, start, end, format='pandas', view='stacked')





