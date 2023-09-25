from FinForecast import Share
from FinForecast import Historical_stock as hist
import pandas as pd

ticker = 'TROX'
path_to_df_historical = '~/Documents/finboys/_Output/TROX_2020_pour_input_arima.pickle'
df_historical = pd.read_pickle(path_to_df_historical)

df_today = hist.get_todays_close_as_df(ticker)
pred = Share.ARIMA_prediction(df_today, df_historical, path_to_df_historical, ARIMA_order= (2,0,5))

subject = 'Prediction du jour'
message = "Le modele predit que {} cloturera a {:.2f} USD le {}".format(ticker, pred, str(Share.infivedays()))
destinataires = ['francoisroyca@gmail.com', 
                'victor.m.cerdacarvajal@gmail.com',
                'thomas.brown.05@gmail.com', 
                'finboys.news@gmail.com'
                ]

Share.by_mail(subject, message, receiver_email=destinataires)