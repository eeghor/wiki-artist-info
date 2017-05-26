import wikipedia
import requests
import re
from bs4 import BeautifulSoup

artists = "air deftones interpol sia editors".split()

for a in artists:

    url = wikipedia.page(a + " (band)").url
    r = requests.get(url).text  # response body as bytes so need get text first

    soup = BeautifulSoup(r, "lxml")

    years_span = soup.find("span", string=re.compile('^Years'))
    years = years_span.parent.next_sibling.next_sibling.text
    print(years)

    try:
        brn  = soup.find("th", string=re.compile('^Born'))
        if not brn:
            print('found no born')
        else:
            print(brn)
            print(brn.next_sibling.next_sibling.text)
    except:
        pass

    try:
        mmb  = soup.find("th", string=re.compile('^Members'))
        if not mmb:
            print('found no members')
        else:
            print([l.strip().lower() for l in mmb.next_sibling.next_sibling.text.split("\n") if l.strip()])
    except:
        pass 


    try:
        lab  = soup.find("th", string=re.compile('^Labels'))
        if not lab:
            print('found no labels')
        else:
            print([l.strip().lower() for l in lab.next_sibling.next_sibling.text.split("\n") if l.strip()])
    except:
        pass 