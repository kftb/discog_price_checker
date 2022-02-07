import discogs_client

import os
from dotenv import load_dotenv

load_dotenv()

USER_TOKEN = os.getenv('USER_TOKEN')

d = discogs_client.Client("ebayka/0.1", user_token=USER_TOKEN)

def ingestRecordNames():
    titles = []
    titles.append('Binh Dreifach')
    queryApi(titles)

def queryApi(titles): 
    
    for item in titles:
        results = d.search(item, type='release')
        results.pages
        artist = results[0].artists[0]
        artist.name

        for release in results:
            # print(release.label)
            print(release.marketplace_stats.lowest_price)
            print(release.price_suggestions)
            
def getValue(releaseID):
    results = d.search('8188037', type='release')

ingestRecordNames()
