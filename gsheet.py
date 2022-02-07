# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def main():

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('Discog Price Checker')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.worksheet('Input')

    val = sheet_instance.acell('B1').value
    print(val)

    # get all the records of the data
    records_data = sheet_instance.get_all_records()

    # view the data
    records_data

    return records_data

main()