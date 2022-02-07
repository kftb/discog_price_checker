import os
import sys
import datetime;
import discogs_client
import gsheet
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(handlers=[logging.FileHandler("api.log"), logging.StreamHandler()], level=logging.DEBUG)

USER_TOKEN = os.getenv('USER_TOKEN')

d = discogs_client.Client("ebayka/0.1", user_token=USER_TOKEN)

def main():
    logging.info('-------------------------------------------------------------')
    logging.info('-------------------------------------------------------------')

    # Read the data from Google Sheets
    logging.info('Kick-off data collection')
    records_input = gsheet.readInput()

    # Collect pricing information
    logging.info('Kick-off Discog data call')
    records_with_prices = queryApi(records_input)

    # Pass data back to Google Sheets
    logging.info('Pass %s searched entries to Google Sheets', str(len(records_with_prices)))
    gsheet.writeOutput(records_with_prices)

def queryApi(titles): 

# ct stores current time
    ts = datetime.datetime.now()
    logging.info('---------------------------------')
    logging.info('Beginn processing at %s', str(ts))
    
    for count, item in enumerate(titles):
        logging.info('Beginn processing search term #%s: %s ', str(count), str(item["nameOfRecord"]))
        api_return = d.search(item["nameOfRecord"], type='release')
        api_return.pages
        results = api_return
        artist = results[0].fetch('artists')

        titles[count]['record_id'] = results[0].id
        titles[count]['matched_title'] = results[0].title
        titles[count]['matched_artist'] = artist[0]['name']
        titles[count]['timestamp'] = str(ts)

        prices = getattr(results[0], 'price_suggestions', 'n/a')
        titles[count]['price_poor'] = prices.poor.value
        titles[count]['price_fair'] = prices.fair.value
        titles[count]['price_good'] = prices.good.value
        titles[count]['price_very_good'] = prices.very_good.value
        titles[count]['price_near_mint'] = prices.near_mint.value
        titles[count]['price_mint'] = prices.mint.value
    
    logging.info('Finished processing all search terms')
    return(titles)
            
main()
