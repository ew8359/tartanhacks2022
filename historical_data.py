import time
import datetime
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
def historical_data(tinker):
    period1 = int(time.mktime(datetime.datetime(2021, 2, 4, 23, 27).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2022, 2, 5, 23, 27).timetuple()))
    interval = '1d'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{tinker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    L = list(df["Close"])
    res = []
    for s in L:
        res.append(float(s))
    return res #return a list

