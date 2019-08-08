from quantea.db.models import Stock
from pymongo.errors import BulkWriteError
from collections import namedtuple
from functools import partial
import pymongo
import json

def json_object_hook(data):
    return json.loads(data, object_hook=lambda d: namedtuple('X', ['_'.join(x.split('-')).lstrip('_') if x != 'class' and x != 'type' and x != 'for' and x != 'id' else x + 's' for x in d.keys()])(*d.values()))
    # return namedtuple('X', d.keys())(*d.values())

def should_call_api(tickers, start_date, end_date):
    """
    Checks whether querys should be called 
    """
    SPY_query_set = Stock.objects.raw({'ticker': 'SPY', 'date': {"$gte": start_date, "$lte": end_date}})
    spy_results = SPY_query_set.aggregate({'$sort': {'date': pymongo.DESCENDING}})
    trading_days = list(spy_results)


    for ticker in tickers:
        try:
            query_set = Stock.objects.raw({'ticker': ticker, 'date': {"$gte": start_date, "$lte": end_date}})
            results = list(query_set.aggregate({'$sort': {'date': pymongo.DESCENDING}}))

            if len(results) == 0: # stock does not exist
                return True
            if len(trading_days) == 0: # SPY does not exist
                return True

            if results[0]['date'] < trading_days[0]['date']:
                return True
            elif results[-1]['date'] > trading_days[-1]['date']:
                return True
        except Stock.DoesNotExist:
            return True
    return False

def save_stocks(stocks):
    try:
        Stock.objects.bulk_create(stocks)
    except BulkWriteError:
        for stock in stocks:
            try:
                result = Stock.objects.get({'_id': stock.key})
                # result.update(stock)
            except Stock.DoesNotExist:
                stock.save()

def extract_stock(stock_df):
    stocks = []
    for _, row in stock_df.iterrows():
        stocks.append(Stock(key=row.key, ticker=row.ticker, close=row.close, volume=row.volume, date=row.date.date()))
    return stocks

def store_stocks_data(stocks_df, stock_names):
    stocks = []
    for ticker in stock_names:
        stored_stock = stocks_df[ticker].reset_index()
        stored_stock['ticker'] = ticker
        stored_stock['key'] = ticker + '-' + stored_stock.date.astype(str)

        stocks += extract_stock(stored_stock)

    save_stocks(stocks)
    

def store_stock_data(stock_df, stock_name):
    stored_stock = stock_df.reset_index()
    stored_stock['ticker'] = stock_name
    stored_stock['key'] = stock_name + '-' + stored_stock.date.astype(str) 

    stocks = extract_stock(stored_stock)

    save_stocks(stocks)




