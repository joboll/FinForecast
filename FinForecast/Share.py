from __future__ import print_function
from yahoofinancials import YahooFinancials
import pandas as pd
import smtplib, ssl
from datetime import date, timedelta
import pickle

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import discovery
from pprint import pprint

from FinForecast import ArimaForecast as af
from FinForecast import Historical_stock as hist


def ARIMA_prediction(df_today, df_historical, path_to_df_historical, ARIMA_order= (3,0,6), window_size=92, lag= 5):
    """
    Take a dataframe of the historical data of a stock to return ARIMA price foretcast in 5 days.
    """
    return_label = 'rtn{}'.format(lag)

    # Add today's data to historical data
    df_historical = df_historical.append(df_today)

    # Calcul today's return with {lag} days ago
    todays_close = df_historical['close'].iloc[-1]
    five_days_ago_close = df_historical['close'].iloc[-6]
    todays_return5 = ( ( todays_close / five_days_ago_close ) - 1) * 100 
    df_historical[return_label].iloc[-1] = todays_return5

    # Transform (find) today's mean deviation return
    todays_transformed_return = todays_return5 - df_historical.iloc[-12:, 1].mean()
    df_historical['meanDev'].iloc[-1] = todays_transformed_return

    # Forecast (transformed return format)
    transformed_forecast = af.arima_forecast(df_historical['meanDev'], ARIMA_order= ARIMA_order, window_size= window_size)

    # Reverting the transformation to get closing price in 5 days
    erreur = todays_transformed_return - transformed_forecast
    pred_rtn5 = todays_return5 - erreur
    predicted_price_in_five_days = todays_close + (todays_close * (pred_rtn5 / 100))

    # Save the new df_historical
    df_historical.to_pickle(path_to_df_historical)

    return predicted_price_in_five_days.iloc[0]

def by_mail(subject, message, sender_email= 'finboys.news@gmail.com', receiver_email=  'finboys.news@gmail.com', smtp_ssl= "smtp.gmail.com"):
    """Send a simple email to recipient through secure SSL.
    """
    
    port = 465  # For SSL
    password = "***"
    sender_email = sender_email
    receiver_email = receiver_email
    message = """\
    Subject: {subject}

    {message}""".format(subject= subject, message= message)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_ssl, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def by_ggsheet(values, file_id, range_, value_input_option= 'RAW', insert_data_option= 'OVERWRITE'):
    """Add (append) values to google spreadsheet.

        Parameters:
            values (list): list of values to append. https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values
            file_id (str): Spreadsheet URL between d/ ... /edit
            range_: A1 notation of the range of field to apply append method. Will be first empty row of 
                column A anyway because it's what spreadsheets.values.append does.
    """

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('_Credentials/token.pickle'):
        with open('_Credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '_Credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('_Credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to update.
    spreadsheet_id = file_id  


    value_range_body = {
    "range": range_,
    "majorDimension": 'ROWS',
    "values": values,
    }

    request = service.spreadsheets().values().append(spreadsheetId= file_id, 
                                                    range= range_, 
                                                    valueInputOption= value_input_option, 
                                                    insertDataOption= insert_data_option, 
                                                    body= value_range_body
                                                    )
    response = request.execute()
