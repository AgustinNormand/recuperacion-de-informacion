from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class Netcraft_Collector():
    def __init__(self):
        self.netcraft_url = "https://trends.netcraft.com/topsites"

    def collect_links(self, limit):
        html_page = requests.get(self.netcraft_url)
        soup = BeautifulSoup(html_page.text, "html5lib")
        table = soup.find_all("table", {'class':"table-topsites"})[0]

        top_links = []

        for tr in table.find_all("tr")[1:]:
            top_links.append(tr.find_all("td")[1].find("a").get('href'))
        return top_links[:limit]
