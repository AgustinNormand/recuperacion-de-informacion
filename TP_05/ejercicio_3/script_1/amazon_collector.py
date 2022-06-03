from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class Amazon_Collector():
    def __init__(self):
        self.amazon_url = "https://www.amazon.com"

    def collect_links(self, link):
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        result_links = []
        html_page = requests.get(link, headers=headers, timeout=3)
        soup = BeautifulSoup(html_page.text, "html5lib")
        for link in soup.findAll('a'):
            href = link.get('href')
            parsed_uri = urlparse(href)

            if str(href).startswith("/"):
                result_links.append(self.amazon_url+href)
            else:
                if str(parsed_uri.netloc) == "www.amazon.com":
                    result_links.append(href)

        return result_links