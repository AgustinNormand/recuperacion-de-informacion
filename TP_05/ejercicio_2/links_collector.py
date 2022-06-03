from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class Links_Collector():
    def __init__(self):
        '''self.proxies = {
            "http"  : "http://proxy.unlu.edu.ar",
            "https" : "https://proxy.unlu.edu.ar",
        }'''

    def valid_href(self, href):
        if href == None:
            return False
        if href.startswith("#"):
            return False

        return True

    def absolute_href(self, href):
        #return "http" in href or "https" in href or "://" in href
        return bool(urlparse(href).netloc)

    def to_absolute(self, href, host):
        return host+href

    def collect_links(self, url):
        # html_page = requests.get(url, proxies=self.proxies)
        try:
            html_page = requests.get(url, timeout=5)
        except:
            return []
        parsed_uri = urlparse(url)
        host = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        soup = BeautifulSoup(html_page.text, "html5lib")
        links = []
        for link in soup.findAll('a'):
            href = link.get('href')
            if self.valid_href(href):
                if self.absolute_href(href):
                    links.append(href)
                else:
                    links.append(self.to_absolute(href, host))
        return links
