from db.models import Stock
import pymongo
import pandas as pd
import time
import numpy as np

def get_stock_date_for_period(tickers, start_date, end_date, format='pandas', view='flat'):
    """
    Checks whether querys should be called 
    """

    df_market = pd.DataFrame(columns=['date', 'close' , 'volume', 'ticker'])
    try:
        query_set = Stock.objects.raw({'$or': [{'ticker': ticker} for ticker in tickers], 'date': {"$gte": start_date, "$lte": end_date}})
        results = query_set.aggregate({'$sort': {'date': pymongo.ASCENDING}})
        df_market = pd.DataFrame(list(results))
        df_market = df_market[['date', 'ticker', 'close', 'volume']]

        if view == 'stacked':
            df_market = df_market.\
                groupby(['date', 'ticker'], as_index=True).\
                first().\
                unstack(level=1)
            df_market.columns = df_market.columns.swaplevel(0,1)

        return df_market
        
    except Stock.DoesNotExist:
        raise ValueError("Stock does not exist {ticker}".format(ticker=tickers))