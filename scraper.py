import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url_base = 'https://www.nulled.to/topic/'
url_extra = '515844-hurr1s-refunding-cave-10-fastest-responding-refunder-amazoncomcaukauold-orders-macysbestbuytargetnordstormwalmartnike-and-many-more/'
response = requests.get(url_base + url_extra)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())

url_extra = url_extra + 'page-1' if url_extra[-1] == '/' else url_extra
with open(f'CaaS/{url_extra}.html', 'w+') as file:
    file.write(soup.prettify())
