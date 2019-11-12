import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url_base = 'https://www.nulled.to/topic/'
url_extra = '783730-robomans-refunding-service-10-high-success-rates-quick-response-best-and-cheap-amazon-bestbuy-nike-many-more/'
response = requests.get(url_base + url_extra)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())

url_extra = url_extra + 'page-1' if url_extra[-1] == '/' else url_extra
with open(f'html/{url_extra}.html', 'w+') as file:
    file.write(soup.prettify())