import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url_base = 'https://www.nulled.to/topic/'
url_extra = '830359-trengods-refunding-service-cheapest-rates-fast-quick-communication-worldwide/page-4'
response = requests.get(url_base + url_extra)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())

url_extra = url_extra + 'page-1' if url_extra[-1] == '/' else url_extra
with open(f'html/{url_extra}.html', 'w+') as file:
    file.write(soup.prettify())