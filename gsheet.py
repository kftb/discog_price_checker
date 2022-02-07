# importing the required libraries
import enum
import sys
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import logging

logging.basicConfig(handlers=[logging.FileHandler("api.log"), logging.StreamHandler()], level=logging.DEBUG)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

def readInput():

    logging.info('%s before you %s', 'Look', 'leap!')
    logging.info('Opened Google Sheets')
    # get the instance of the Spreadsheet
    sheet = client.open('Discog Price Checker')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.worksheet('Input')

    # get all the records of the data
    logging.info('Get all records')
    records_data = sheet_instance.get_all_records()

    # filter the data to 'Yes' 
    filtered = [d for d in records_data if condition(d)]

    logging.info('Return %s filtered entries', str(len(filtered)))
    return filtered

def condition(dic):

    # return only fields that are marked with Yes
    return dic['search'] == 'Yes'

def writeOutput(records_with_prices):
    logging.info("Begin Google Sheets processing")
    # get the instance of the Spreadsheet
    sheet = client.open('Discog Price Checker')

    # get first row to write data to
    si = sheet.worksheet('config')
    lastRow = si.acell('C3').value
    logging.info("First empty row is " + str(lastRow))

    # get the first sheet of the Spreadsheet
    si = sheet.worksheet('Output')

    # iterate over results and write output
    for count, item in enumerate(records_with_prices):
        logging.info("Writing results for search term %s to Google Sheets", item['nameOfRecord'])

        rowValue = 'C'+str(int(lastRow)+count)+':Z'+str(int(lastRow)+count)
        print(rowValue)
        si.update(rowValue, [[item['nameOfRecord'], 
            item['timestamp'],
            item['record_id'],
            item['matched_title'],
            item['matched_artist'],
            item['price_lowest'],
            item['price_poor'],
            item['price_fair'],
            item['price_good'],
            item['price_very_good'],
            item['price_very_good_plus'],
            item['price_near_mint'],
            item['price_mint'],
            ]])
    logging.info("Completed API run.")

# writeOutput([{'nameOfRecord': 'Binh Dreifach', 'search': 'Yes', 'record_id': 8188037, 'matched_title': 'Dreifach', 'matched_artist': 'Binh', 'price_lowest': '4.59', 'price_suggested': '11.39', 'timestamp': '2022-02-06'
# }])
