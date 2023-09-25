from FinForecast import Share
from FinForecast import Historical_stock as Hist
#import pandas as pd


ticker = ['TROX', 'CC', 'HPQ.V', 'BAD.TO']
tab = ['TROX_data', 'CC_data', 'HPQ_data', 'BAD_data']

"""Init

for ticker, tab in zip(ticker, tab):
    data = Hist.get_ohlc_as_tuple(ticker, 
                                  start_date= '2015-01-01')
                                  )
    Share.by_ggsheet(data, 
                    '1fj0fJu8DEYuLXNiefXLWOqExtEQZjX5I4eMhHGz-jJI', 
                    tab)
"""

for ticker, tab in zip(ticker, tab):
    data = Hist.get_ohlc_as_tuple(ticker, 
                                  start_date= str(Hist.today())
                                  )
    Share.by_ggsheet(data, 
                    '1fj0fJu8DEYuLXNiefXLWOqExtEQZjX5I4eMhHGz-jJI', 
                    tab)