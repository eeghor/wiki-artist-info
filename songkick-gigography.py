import requests
import json
from bs4 import BeautifulSoup

SONGKICK_API_KEY = "xA3m029StZXk8u3V"

ARTIST = "placebo"

search_str = 'http://api.songkick.com/api/3.0/search/artists.json?query=' + ARTIST + '&apikey=' + SONGKICK_API_KEY

print(search_str)

r = requests.get(search_str).text  # response body as bytes so need get text first

res = json.loads(r)["resultsPage"]["results"]["artist"][0]

artist_id = str(res["id"])

GIG_STR = "http://api.songkick.com/api/3.0/artists/" + artist_id + "/gigography.json?apikey=" + SONGKICK_API_KEY
r = requests.get(GIG_STR).text


#soup = BeautifulSoup(r, "lxml")

print(r)