#from netcraft_collector import *
from amazon_collector import *
from BTrees.OOBTree import OOBTree
#from urllib.parse import urlparse
#from pyvis.network import Network
#import networkx as nx
import time
import json

class Amazon_Crawler():
    def __init__(self, TOTAL_MAX_PAGES):
        self.TOTAL_MAX_PAGES = TOTAL_MAX_PAGES

        self.queue = [["https://www.amazon.com", 0]]

        self.collected_pages = 0
        self.lc = Amazon_Collector()
        self.wrong_urls = []
        self.btree = OOBTree()

        self.last_export = 0

        self.begin_crawl()

        print("Crawl Ended")

    def begin_crawl(self):
        while self.queue != [] and self.collected_pages < self.TOTAL_MAX_PAGES:
            try:
                link, depth = self.queue.pop(0)

                print("Collected Pages {}, Processing {}".format(self.collected_pages, link))

                if link in self.btree:
                    continue

                collected_links = self.lc.collect_links(link)
                self.btree[link] = [depth, collected_links]

            except Exception as e:
                print(e)
                self.wrong_urls.append(link)
            self.collected_pages += 1

            collected_links_with_depth = []
            for link in collected_links:
                collected_links_with_depth.append([link, depth+1])
            self.queue.extend(collected_links_with_depth)

            if abs(self.last_export - self.collected_pages) >= 30:
                self.export_btree()

    def export_btree(self):
        dictionary_btree = {}
        for key in self.btree:
            dictionary_btree[key] = {}
            dictionary_btree[key]["depth"] = list(self.btree[key])[0]
            dictionary_btree[key]["links"] = list(self.btree[key])[1]

        with open("btree.json", "w") as outfile:
            json.dump(dictionary_btree, outfile)
