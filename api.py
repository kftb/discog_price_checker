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

    logging.info('Beginn processing at %s', str(ts))
    
    for count, item in enumerate(titles):
        logging.info('Beginn processing search term #%s: %s ', str(count), str(item["nameOfRecord"]))
        api_return = d.search(item["nameOfRecord"], type='release')
        api_return.pages
        print(api_return)
        results = api_return
        artist = results[0].artists[0]
        titles[count]['record_id'] = results[0].id
        titles[count]['matched_title'] = results[0].title
        titles[count]['matched_artist'] = artist.name
        titles[count]['timestamp'] = str(ts)

        for release in results:
            titles[count]['price_lowest'] = release.marketplace_stats.lowest_price.value
            titles[count]['price_poor'] = release.price_suggestions.poor.value
            titles[count]['price_fair'] = release.price_suggestions.fair.value
            titles[count]['price_good'] = release.price_suggestions.good.value
            titles[count]['price_very_good'] = release.price_suggestions.very_good.value
            titles[count]['price_very_good_plus'] = release.price_suggestions.very_good_plus.value
            titles[count]['price_near_mint'] = release.price_suggestions.near_mint.value
            titles[count]['price_mint'] = release.price_suggestions.mint.value
        logging.info('-------------------------------------------------------------')
    
    logging.info('Finished processing all search terms')
    return(titles)
            
main()
