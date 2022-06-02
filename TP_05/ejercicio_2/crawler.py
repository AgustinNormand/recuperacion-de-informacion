from netcraft_collector import *
from links_collector import *
from BTrees.OOBTree import OOBTree
from urllib.parse import urlparse
from pyvis.network import Network
import networkx as nx

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

        self.begin_crawl()

        self.pageids = {}
        self.create_pageids()

        self.create_graph()

    def get_url_physical_depth(self, url):
        path = urlparse(url).path
        return path.count("/")

    def begin_crawl(self):
        while self.queue != [] and self.collected_pages < self.TOTAL_MAX_PAGES:
            try:
                link, depth = self.queue.pop(0)

                if depth > self.MAX_LOGICAL_DEPTH:
                    continue

                if self.get_url_physical_depth(link) > self.MAX_PHYSICAL_DEPTH:
                    continue

                if link in self.btree:
                    continue

                collected_links = self.lc.collect_links(link)[:self.MAX_PAGES_PER_SITE]
                self.btree[link] = collected_links
            except:
                self.wrong_urls.append(link)
            self.collected_pages += 1

            collected_links_with_depth = []
            for link in collected_links:
                collected_links_with_depth.append([link, depth+1])
            self.queue.extend(collected_links_with_depth)

    def create_pageids(self):
        id_acum = 0
        for key in list(self.btree.keys()):
            if not key in self.pageids.keys():
                    self.pageids[key] = id_acum
                    id_acum += 1
            for value in list(self.btree[key]):
                if not value in self.pageids.keys():
                    self.pageids[value] = id_acum
                    id_acum += 1

    def create_graph(self):
        edges = []
        for key in list(self.btree.keys()):
            for value in list(self.btree[key]):
                edges.append((self.pageids[key], self.pageids[value]))

        net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

        #group = 0
        #for key in list(self.btree.keys()):
        #    group += 1
        #    net.add_node(self.pageids[key], label=key, group=group)
        #    for value in list(self.btree[key]):
        #        net.add_node(self.pageids[value], label=value, group=group)

        for key in self.pageids.keys():
            net.add_node(self.pageids[key], label=key)

        net.add_edges(edges)
        net.show('webGraph.html')
