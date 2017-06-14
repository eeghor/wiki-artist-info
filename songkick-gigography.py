"""
Using the Songkick API to collect gigorgaphies
"""

import requests
import json

SONGKICK_API_KEY = "xA3m029StZXk8u3V"

ARTIST = "placebo"

# first, search for an artist - this is needed because we have to have an artist ID before asking for gig data
search_str = 'http://api.songkick.com/api/3.0/search/artists.json?query=' + ARTIST + '&apikey=' + SONGKICK_API_KEY
r = requests.get(search_str).text  # response body as bytes so need get text first

res = json.loads(r)["resultsPage"]["results"]["artist"][0]  # take the top search result

artist_id = str(res["id"])

GIG_STR = "http://api.songkick.com/api/3.0/artists/" + artist_id + "/gigography.json?apikey=" + SONGKICK_API_KEY
r = requests.get(GIG_STR).text

print(r)