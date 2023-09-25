import pandas as pd
from yahoofinancials import YahooFinancials
from datetime import date, timedelta

from FinForecast import Share
from FinForecast import ArimaForecast as af

def today():
    today = date.today()
    return today

def tomorrow(today= today()):
    delay = timedelta(days=1)
    tomorrow = today + delay
    return tomorrow

def infivedays(today= today(), delay= timedelta(days=7)):
    date_infivedays = today + delay
    return date_infivedays

def get_todays_close_as_df(ticker):
    """Returns a simple dataframe of today's date as index and ticker's close as value.
        Parameter:
            ticker (str): Official stock market ticker. Ex.: 'TROX'
        Exemple:
                        close
            2020-09-04   9.27
    """
    # Get today's close price
    yahoo_financials = YahooFinancials(ticker)
    data_today = yahoo_financials.get_historical_price_data(start_date= str(today()),  
                                                            end_date= str(tomorrow()),  
                                                            time_interval='daily') 

    # Extracting the data out of the dictionnary
    date = [data_today[ticker]['prices'][-1]['formatted_date']]
    close = [data_today[ticker]['prices'][-1]['close']]

    # Create today's df with today's data
    df_today = pd.DataFrame(data= close, index= date, columns= ['close'])

    return df_today

def get_ohlc_as_df(ticker, start_date= '2015-01-01', end_date= str(tomorrow()), time_interval= 'daily'):
    """Returns a dataframe of ticker's historical values with datetime index.

        Parameter:
            ticker (str): Official stock market ticker. Ex.: 'TROX'
        Exemple Output:
                        high     low   open  close   volume  adjclose
            Date                                                                      
            2018-01-02  21.04  20.32  20.55  20.94  1802500     19.76
            2018-01-03  21.49  20.87  21.00  21.21  1258300     20.02
    """
    yahoo_financials = YahooFinancials(ticker)
    data = yahoo_financials.get_historical_price_data(start_date= start_date, 
                                                    end_date= end_date, 
                                                    time_interval= time_interval)

    # Extraire 'price' keys du dict vers un df
    df = pd.DataFrame(data[ticker]['prices'])

    # Remplacer 'formatted_date' col par 'Date'
    col = list(df.columns) 
    col[-1] = 'Date'
    df.columns = col

    # Set index to 'Date'
    df = df.drop('date', axis=1).set_index('Date')
    df.index = pd.to_datetime(df.index)

    return df

def get_ohlc_as_tuple(ticker, start_date= '2015-01-01', end_date= str(tomorrow()), time_interval= 'daily'):
    
    yahoo_financials = YahooFinancials(ticker)
    data_today = yahoo_financials.get_historical_price_data(start_date= start_date,  
                                                            end_date= end_date,  
                                                            time_interval= time_interval) 

    date = [ i['formatted_date'] for i in data_today[ticker]['prices']]
    high = [ i['high'] for i in data_today[ticker]['prices']]
    low = [ i['low'] for i in data_today[ticker]['prices']] 
    open_ = [ i['open'] for i in data_today[ticker]['prices']]
    close_ = [ i['close'] for i in data_today[ticker]['prices']]
    volume = [ i['volume'] for i in data_today[ticker]['prices']]
    adjclose = [ i['adjclose'] for i in data_today[ticker]['prices']]

    ohlc_tuple =  tuple(zip(date, high, low, open_, close_, volume, adjclose))
    #ohlc_list = [list(i) for i in ohlc_tuple]

    return ohlc_tuple
