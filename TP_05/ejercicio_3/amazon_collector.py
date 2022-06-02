from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class Amazon_Collector():
    def __init__(self):
        self.amazon_url = "https://www.amazon.com"

    def collect_links(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        }

        html_page = requests.get(self.amazon_url, headers=headers)
        #print(html_page.text)
        soup = BeautifulSoup(html_page.text, "html5lib")
        for link in soup.findAll('a'):
            href = link.get('href')
            print(href)