import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def rowBuilder(paymentName, paymentAoumt, sourceFile):
    firstColumn = []
    
    for i in paymentName:
        firstColumn.append([i]) 

    listNum = 0
    finalSheet = []

    for r in paymentAoumt:
        if(listNum >= len(paymentName)):
          break
        burnerList = []
        burnerList = firstColumn[listNum]
        burnerList.append(r)
        finalSheet.append(burnerList)
        listNum += 1 
    
    update_values(
        googleSheetCreation(sourceFile),
        "A1",
        "USER_ENTERED",
        finalSheet,
    )
    



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 'https://www.googleapis.com/auth/drive']


def googleSheetCreation(sourceFile):
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  
  if os.path.exists("googleSheetsToken/token.json"):
    creds = Credentials.from_authorized_user_file("googleSheetsToken/token.json", SCOPES)
 
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("googleSheetsToken/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    todays_date = datetime.date.today()
    
    title = f"{sourceFile} {todays_date}"
    service = build("sheets", "v4", credentials=creds)
    spreadsheet = {"properties": {"title": title}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
    print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
    
    return spreadsheet.get("spreadsheetId")
  except HttpError as err:
    print(err)



def update_values(spreadsheet_id, range_name, value_input_option, _values):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = Credentials.from_authorized_user_file("googleSheetsToken/token.json", SCOPES)
  
  try:
    service = build("sheets", "v4", credentials=creds)
    values = _values
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


