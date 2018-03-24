import networkx as nx
import gartner_ds_parser as gp
import itertools
import pprint
# class for a company
import cPickle
import pickle
import config
from serialize import dump, load
from entity import company


class network:

    def __init__(self, init=False):
        self.save_file = None
        self.G = None
        return

    def create_network(self):
        self.G = nx.Graph()
        self.save_model()
        return

    def save_model(self):
        print '> ', self.save_file
        # save the network
        with open(self.save_file, "wb") as f:
            cPickle.dump(self.G, f)
        return

    def load_model(self):
        if self.G is None:
            self.create_network()
        with open(self.save_file, "rb") as f:
            self.G = cPickle.load(f)
        return


# -------------------------------------------------- #

class company_network(network):

    def __init__(self, init=False):
        network.__init__(self, init)
        self.save_file = config.company_network_file

        if init:
            self.create_network()
        else:
            self.load_model()

        return

    def get_network_info(self):
        print 'Number of nodes', self.G.number_of_nodes()
        print 'Number of edges', self.G.number_of_edges()

    def create_network(self):

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

        self.save_model()
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


# -------------------------------------------------- #

class product_network(network):
    def __init__(self, init=False):
        network.__init__(self, init)
        return

    def create_network(self):
        return


# -------------------------------------------------- #

# -------------------------------------------------- #


def dummy_test():
    network_obj = company_network(True)
    network_obj.get_network_info()
    test_list = ['Facebook', 'ABB', 'NASA', 'Teradata', 'Yahoo', 'Zebra Medical Vision', 'Palantir']
    for t in test_list:
        print 'Company :: ', t
        print network_obj.get_sim_companies(t)
    # print network_obj.get_node('Yahoo').display()


dummy_test()
