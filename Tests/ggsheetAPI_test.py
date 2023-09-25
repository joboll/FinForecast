from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery

#Client ID: 170749229512-n0cfth4rp2p7blfoqmbdvtsahpaku6kb.apps.googleusercontent.com
#Client secret: Fj9-tSHCp9F56tEINvSIgqVF

# TODO: Change placeholder below to generate authentication credentials. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
#
# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/spreadsheets'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# https://www.googleapis.com/auth/spreadsheets.readonly

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


#if os.path.exists('token.pickle'): 
#    with open('token.pickle', 'rb') as token: 
#        creds = pickle.load(token) 

service = discovery.build('sheets', 'v4', credentials=creds)

# The ID of the spreadsheet to update.
spreadsheet_id = '1fj0fJu8DEYuLXNiefXLWOqExtEQZjX5I4eMhHGz-jJI'  

# The A1 notation of a range to search for a logical table of data.
# Values will be appended after the last row of the table.
range_ = 'TROX_data!B:B'

# How the input data should be interpreted.
value_input_option = 'RAW'  

# How the input data should be inserted.
insert_data_option = 'OVERWRITE' 

value_range_body = {
  "range": "TROX_data!B:B",
  "majorDimension": "ROWS",
  "values": [
    [9.3]
  ],
}

request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, 
                                                range=range_, 
                                                valueInputOption=value_input_option, 
                                                insertDataOption=insert_data_option, 
                                                body=value_range_body
                                                )
response = request.execute()

# TODO: Change code below to process the `response` dict:
pprint(response)