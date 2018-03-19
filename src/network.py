import networkx as nx
import gartner_ds_parser as gp
import itertools
import pprint
# class for a company
import cPickle
import config

class hyponym:

    def __init__(self,_name,_class=None):
        self._name = _name
        self._class = _class
        return

    def set_class(self,_class):
        self._class = _class
        return

    def display(self):
        print ' hyponym / instance :: ', self._name, ' class ::', self._class
        return

    def set_text(self , text_dict):
        self.text_dict = text_dict

    def get_text_dict(self):
        return self.text_dict


class network():

    def __init__(self, init=False):
        self.G = None
        if init :
            self.create_seed_network()
            self.save_model()
        else :
            self.load_model()
        return

    def get_network_info(self):
        print 'Number of nodes', self.G.number_of_nodes()
        print 'Number of edges', self.G.number_of_edges()

    def save_model(self):
        # save the network
        with open(config.network_file,"wb") as f :
            cPickle.dump(self.G, f)
        return

    def load_model(self):
        with open(config.network_file,"rb") as f:
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
            for h in data['hyponym']:
                node = hyponym(h, data['class'])
                node_list.append(node)

            edge_list = list(itertools.combinations(node_list, 2))

            self.G.add_nodes_from(node_list)
            for e in edge_list:
                self.G.add_edge(e[0],e[1],weight=1)

        return


network_obj = network(False)
network_obj.get_network_info()



# Todo : Define the bootstrap function with the seed graph using the data provided from Twitter
