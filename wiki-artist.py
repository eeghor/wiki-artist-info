import wikipedia
import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import time

# read up a json artist file
artist_list = list(json.load(open("data/artists.json","r")).keys())
n_artists = len(artist_list)

def scrape_infobox(txt2find, soup):

       try:
           right_th  = soup.find("th", string=re.compile('^' + txt2find))
           if right_th:
                res = right_th.next_sibling.next_sibling.text.lower().strip().split("\n")
           else:
               res = None
       except:
           res = None
       return res

def fill_artist_rec(artist_name):

    art_rec = {
        artist_name:
            {
            "birth_name": None,
            "born": None,
            "members": [],
            "years_active": None,
            "labels": []
            }
                }
    try:
        url = wikipedia.page(artist_name + " (band)").url
    except:
        return art_rec

    if url:
        # if managed to get a url
        r = requests.get(url).text  # response body as bytes so need get text first
        soup = BeautifulSoup(r, "lxml")
        art_rec[artist_name]["birth_name"] = scrape_infobox('Birth', soup)
        art_rec[artist_name]["born"] = scrape_infobox('Born', soup)
        art_rec[artist_name]["members"] = scrape_infobox('Members', soup)
        art_rec[artist_name]["years_active"] = scrape_infobox('Years', soup)
        art_rec[artist_name]["labels"] = scrape_infobox('Labels', soup)

    return art_rec

if __name__ == "__main__":

    artist_wiki = defaultdict(lambda: defaultdict())

    t_start = time.time()

    for i, a in enumerate(artist_list):
        artist_wiki.update(fill_artist_rec(a))
        if (i > 0) and (i%200 == 0):
            print("progress: {:06.0f}/{:06.0f} ({:03.0f}%) - {:03.0f}m {:02.0f}s ".format(i, n_artists, 
                100*i/n_artists, *divmod(time.time() - t_start, 60)))

    json.dump(artist_wiki, open("data/artist_wiki.json", "w"), sort_keys=True, indent=4)


