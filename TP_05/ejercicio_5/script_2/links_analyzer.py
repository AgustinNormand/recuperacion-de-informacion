import json
import networkx as nx
import matplotlib.pyplot as plt



class Links_Analyzer():
    def __init__(self):
        with open('btree.json') as json_file:
            self.btree = json.load(json_file)

        with open('crawl_order.json') as json_file:
            self.crawl_order = json.load(json_file)


        self.pageids = {}
        self.define_pageids()

        self.crawl_order_ids = []
        for value in self.crawl_order:
            self.crawl_order_ids.append(self.pageids[value])

        self.create_graph()

    def define_pageids(self):
        id_acum = 0
        for key in self.btree.keys():
            if not key in self.pageids.keys():
                self.pageids[key] = id_acum
                id_acum += 1

    def overlap(self, list1, list2, total_length):
        intersection = list(set(list1).intersection(set(list2)))
        if len(intersection) == 0:
            return 0
        else:
            #print("Length list1: {}, Length list2: {}, Interseciton {}, Percentage {}".format(len(list1), len(list2), len(intersection), (len(intersection)*100)/total_length))
            return (len(intersection)*100)/total_length

    def create_graph(self):
        G = nx.DiGraph()
        nodes = range(len(self.pageids))

        edges = []
        for key in list(self.btree.keys()):
            for value in list(self.btree[key]):
                if value in self.pageids.keys():
                    edges.append((self.pageids[key], self.pageids[value]))
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        pr = nx.pagerank(G, alpha=0.8, max_iter=100)
        #print("PageRank:{}".format(len(pr)))
        h, a = nx.hits(G, max_iter=200)
        #print("hub:{}".format(len(h)))
        #print("auth:{}".format(len(a)))

        len_of_lists = len(pr)

        x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        a_overlap = []
        pr_overlap = []
        crawl_overlap = []

        a_sorted = dict(sorted(a.items(), key=lambda item: item[1]))
        pr_sorted = dict(sorted(pr.items(), key=lambda item: item[1]))

        for i in x:
            index = round((i * len_of_lists) / 100)
            a_overlap.append(self.overlap(list(a_sorted.keys())[:index], list(a_sorted.keys())[:index], len_of_lists))
            pr_overlap.append(self.overlap(list(a_sorted.keys())[:index], list(pr_sorted.keys())[:index], len_of_lists))
            crawl_overlap.append(self.overlap(list(a_sorted.keys())[:index], self.crawl_order_ids[:index], len_of_lists))


        plt.clf()
        plt.figure(1)

        plt.plot(x, a_overlap)
        plt.plot(x, pr_overlap)
        plt.plot(x, crawl_overlap)

        #plt.show()
        plt.savefig("plot.png")

