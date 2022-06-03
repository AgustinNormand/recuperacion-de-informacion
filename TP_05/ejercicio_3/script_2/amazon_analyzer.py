import json
from pyvis.network import Network

class Amazon_Analyzer():
    def __init__(self):
        with open('btree.json') as json_file:
            self.btree = json.load(json_file)

        #self.pageids = {}
        #self.define_pageids()
        #self.create_graph()

    #def define_pageids(self):
    #    id_acum = 0
    #    for key in self.btree.keys():
    #        if not key in self.pageids.keys():
    #            self.pageids[key] = id_acum
    #            id_acum += 1
    #        for value in self.btree[key]:
    #            if not value in self.pageids.keys():
    #                self.pageids[value] = id_acum
    #                id_acum += 1

    #def create_graph(self):
    #    edges = []
    #    for key in list(self.btree.keys()):
    #        for value in list(self.btree[key]):
    #            edges.append((self.pageids[key], self.pageids[value]))
    #
    #    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    #    for key in self.pageids.keys():
    #        net.add_node(self.pageids[key], label=key)
    #
    #    net.add_edges(edges)
    #    net.show('webGraph.html')