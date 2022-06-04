import json
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urlparse


class Amazon_Analyzer():
    def __init__(self):
        with open('btree.json') as json_file:
            self.btree = json.load(json_file)
        #self.pageids = {}
        #self.define_pageids()
        #self.create_graph()

        self.analize_static_or_dinamic()

        self.analize_logical_depth()

        self.analize_fisical_depth()

    def is_dynamic_url(self, url):
        for ch in ["?", "&", "%", "+", "=", "$", "cgi-bin", ".cgi"]:
            if ch in url:
                return True

    def analize_static_or_dinamic(self):
        static_pages = 0
        dinamic_pages = 0
        for key in self.btree:
            if self.is_dynamic_url(key):
                dinamic_pages += 1
            else:
                static_pages += 1
            for value in self.btree[key]["links"]:
                if self.is_dynamic_url(value):
                    dinamic_pages += 1
                else:
                    static_pages += 1
                    
        plt.clf()
        plt.figure(1)
        labels = 'Dynamic', 'Static'
        sizes = [dinamic_pages, static_pages]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.savefig("dynamic_static_distribution.png")

    def analize_logical_depth(self):
        depths = []
        for key in self.btree:
            depths.append(self.btree[key]["depth"])

        plt.clf()
        plt.figure(2)
        plt.hist(depths, range=(min(depths), max(depths)))
        plt.xlabel("TODO")
        plt.ylabel("TODO")
        plt.savefig("logical_depths_distribution.png")

    def get_url_physical_depth(self, url):
        path = urlparse(url).path
        return path.count("/")

    def analize_fisical_depth(self):
        depth_dict = {}
        depths = []
        for key in self.btree:
            try:
                depth_dict[self.get_url_physical_depth(key)] += 1
            except:
                depth_dict[self.get_url_physical_depth(key)] = 1
            depths.append(self.get_url_physical_depth(key))
            for value in self.btree[key]["links"]:
                depths.append(self.get_url_physical_depth(value))
                try:
                    depth_dict[self.get_url_physical_depth(value)] += 1
                except:
                    depth_dict[self.get_url_physical_depth(value)] = 1

        #print(depths)
        plt.clf()
        plt.figure(4)
        plt.hist(depths, bins=len(depth_dict.keys()))
        #plt.xlabel("TODO")
        #plt.ylabel("TODO")
        plt.savefig("fisical_depths_distribution.png")


        #sorted_keys = sorted(depth_dict.keys())
        #values = []
        #for key in sorted_keys:
        #    values.append(depth_dict[key])

        #plt.clf()
        #plt.figure(4)
        #plt.plot(sorted_keys, values)
        #plt.show()

    def define_pageids(self):
        id_acum = 0
        for key in self.btree.keys():
            if not key in self.pageids.keys():
                self.pageids[key] = id_acum
                id_acum += 1
            for value in self.btree[key]["links"]:
                if not value in self.pageids.keys():
                    self.pageids[value] = id_acum
                    id_acum += 1

    def create_graph(self):
        edges = []
        for key in list(self.btree.keys()):
            for value in list(self.btree[key]["links"]):
                edges.append((self.pageids[key], self.pageids[value]))

        #G = nx.DiGraph()
        #nodes = range(len(self.pageids))
        #G.add_nodes_from(nodes)
        #G.add_edges_from(edges)
        #pos = nx.spring_layout(G)
        #options = {
        #    'node_color': 'lightgreen',
        #    'node_size': 1000,
        #    'width': 3,
        #    'arrowstyle': '-|>',
        #    'arrowsize': 12,
        #}
        #nx.draw_networkx(G, arrows=True, **options, cmap=plt.get_cmap('jet'))
        #plt.show()

        #net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
        #for key in self.pageids.keys():
            #net.add_node(self.pageids[key], label=key)
            #net.add_node(self.pageids[key])
        #net.add_edges(edges)
        #net.show('webGraph.html')

        #Crawled 4712