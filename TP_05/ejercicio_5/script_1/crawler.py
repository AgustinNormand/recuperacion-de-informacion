from netcraft_collector import *
from links_collector import *
from BTrees.OOBTree import OOBTree
from urllib.parse import urlparse
from pyvis.network import Network
import networkx as nx
import json

class Crawler():
    def __init__(self, SEED_LIMIT, TOTAL_MAX_PAGES, MAX_PAGES_PER_SITE, MAX_PHYSICAL_DEPTH, MAX_LOGICAL_DEPTH):
        self.TOTAL_MAX_PAGES = TOTAL_MAX_PAGES
        self.MAX_PAGES_PER_SITE = MAX_PAGES_PER_SITE
        self.MAX_PHYSICAL_DEPTH = MAX_PHYSICAL_DEPTH
        self.MAX_LOGICAL_DEPTH = MAX_LOGICAL_DEPTH

        self.queue = []
        nc = Netcraft_Collector()

        for link in nc.collect_links(SEED_LIMIT):
            self.queue.append([link, 0])

        self.collected_pages = 0
        self.lc = Links_Collector()
        self.wrong_urls = []
        self.btree = OOBTree()

        self.crawl_order = []

        self.last_export = 0
        self.begin_crawl()

        print("Crawl Ended")

    def get_url_physical_depth(self, url):
        path = urlparse(url).path
        return path.count("/")

    def begin_crawl(self):
        while self.queue != [] and self.collected_pages < self.TOTAL_MAX_PAGES:
            try:
                link, depth = self.queue.pop(0)

                print("Collected Pages {}, Processing {}".format(self.collected_pages, link))

                if depth > self.MAX_LOGICAL_DEPTH:
                    continue

                if self.get_url_physical_depth(link) > self.MAX_PHYSICAL_DEPTH:
                    continue

                if link in self.btree:
                    continue

                collected_links = self.lc.collect_links(link)[:self.MAX_PAGES_PER_SITE]

                self.crawl_order.append(link)
                self.btree[link] = collected_links
            except:
                self.wrong_urls.append(link)
            self.collected_pages += 1

            collected_links_with_depth = []
            for link in collected_links:
                collected_links_with_depth.append([link, depth+1])
            self.queue.extend(collected_links_with_depth)

            if abs(self.last_export - self.collected_pages) >= 30:
                self.export_btree()
                self.export_crawl_order()

    def export_crawl_order(self):
        with open("crawl_order.json", "w") as outfile:
            json.dump(self.crawl_order, outfile)

    def export_btree(self):
        dictionary_btree = {}
        for key in self.btree:
            dictionary_btree[key] = list(self.btree[key])

        with open("btree.json", "w") as outfile:
            json.dump(dictionary_btree, outfile)