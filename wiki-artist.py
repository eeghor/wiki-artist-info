import wikipedia
import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict

artists = "air deftones interpol sia editors".split()

artist_dic = defaultdict

for a in artists:

    url = wikipedia.page(a + " (band)").url

    r = requests.get(url).text  # response body as bytes so need get text first

    soup = BeautifulSoup(r, "lxml")

    def scrape_infobox(txt2find):

        try:
            right_th  = soup.find("th", string=re.compile('^' + txt2find))
            if right_th:
                res = right_th.next_sibling.next_sibling.text.lower().strip().split("\n")
                # note that res is a list after .split()
                if (len(res) == 1) or (txt2find == "Born"):  # if it's one-liner or Born
                    res = res[0]
            else:
                res = None
        except:
            res = None

        return res

    def fill_artist_rec(artist_name):

        art_rec = {
                    artist_name: 
                        { 
                        "born": None, 
                        "members": [],
                        "years_active": None,
                        "labels": []
                        }
                    }

        art_rec[artist_name]["born"] = scrape_infobox('Born')
        art_rec[artist_name]["members"] = scrape_infobox('Members')
        art_rec[artist_name]["years_active"] = scrape_infobox('Years')
        art_rec[artist_name]["labels"] = scrape_infobox('Labels')

        return art_rec

    print(fill_artist_rec(a))
