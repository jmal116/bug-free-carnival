import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url_base = 'https://hackforums.net/showthread.php?'
url_extra = 'tid=55342'
response = requests.get(url_base + url_extra)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())

url_extra = url_extra + 'page-1' if url_extra[-1] == '/' else url_extra
with open(f'crimeware/{url_extra}.html', 'w+') as file:
    file.write(soup.prettify())
