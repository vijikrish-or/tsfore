def getstockdata(ticker):
    from pandas_datareader._utils import RemoteDataError
    import pandas as pd
    import pandas_datareader as dr
    import datetime
    from datetime import date
    start = datetime.datetime(2020, 2, 1)
    end = date.today() #datetime.datetime(2020, 9, 30)
    success=1
    try:
        df = dr.DataReader(ticker, 'yahoo', start, end, retry_count=0)
        return df, success
    except RemoteDataError:
        success=0
        ticker='AMZN' #invalid ticker is replaced with amazon
        df = dr.DataReader(ticker, 'yahoo', start, end, retry_count=0)
        return df, success
    