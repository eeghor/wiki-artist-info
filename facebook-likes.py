import requests
import re
from bs4 import BeautifulSoup

r = requests.get("https://www.facebook.com/flumemusic/").text  # response body as bytes so need get text first
soup = BeautifulSoup(r, "lxml")

print(soup.find("span", id="PagesLikesCountDOMID").text)
