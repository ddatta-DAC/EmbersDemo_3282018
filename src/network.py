import networkx as nx
import gartner_ds_parser as gp
import itertools
import pprint
# class for a company
import cPickle
import pickle
import config
from serialize import dump, load
from  entity import company



# -------------------------------------------------- #

class company_network():

    def __init__(self, init=False):
        self.G = None
        if init:
            self.create_seed_network()
            self.save_model()
        else:
            self.load_model()
        return

    def get_network_info(self):
        print 'Number of nodes', self.G.number_of_nodes()
        print 'Number of edges', self.G.number_of_edges()

    def save_model(self):
        # save the network
        with open(config.network_file, "wb") as f:
            cPickle.dump(self.G, f)
        return

    def load_model(self):
        with open(config.network_file, "rb") as f:
            self.G = cPickle.load(f)
        return

    def create_seed_network(self):

        # Seed network created using the class name and instances of the Gartner Data set
        # Each company is a node
        # node data is class :: hyponym
        # Weight between nodes of the same class is 1

        self.G = nx.Graph()

        for data in gp.gen_data_to_feed():
            node_list = []
            for h in data['instance']:
                if h == 'nan':
                    continue

                node = company(h, data['class'])
                # check if node exists!
                for g in self.G.nodes():
                    if g.get_name() == h:
                        node = g
                        break
                node.set_text(text_dict=data['text'])
                node_list.append(node)

            edge_list = list(itertools.combinations(node_list, 2))
            self.G.add_nodes_from(node_list)
            for e in edge_list:
                self.G.add_edge(e[0], e[1], weight=1)

        return

    def get_sim_companies(self, cname):
        sim_com_list = []
        for g in self.G.nodes():
            if g.get_name() == cname:
                # get all neighbors of g
                nbrs = self.G.neighbors(g)
                for n in nbrs:
                    sim_com_list.append(n.get_name())

        return sim_com_list

    def get_node(self, c_name):
        for g in self.G.nodes():
            if g.get_name() == c_name:
                return g

# --------------------------------------------- #

def dummy_test():
    network_obj = company_network(True)
    network_obj.get_network_info()
    test_list = ['Facebook', 'ABB', 'NASA', 'Teradata', 'Yahoo', 'Zebra Medical Vision', 'Palantir']
    for t in test_list:
        print 'Company :: ', t
        print network_obj.get_sim_companies(t)
    # print network_obj.get_node('Yahoo').display()

dummy_test()


# Todo : Define the bootstrap function with the seed graph using the data provided from Twitter
