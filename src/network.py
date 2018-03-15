import networkx as nx
import gartner_ds_parser as gp
import itertools
import pprint
# class for a company

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


def create_seed_network():

    # Seed network created using the class name and instances of the Gartner Data set
    # Each company is a node
    # node data is class :: hyponym
    # Weight between nodes of the same class is 1

    G = nx.Graph()
    for data in gp.gen_data_to_feed():
        node_list = []
        for h in data['hyponym']:
            node = hyponym(h, data['class'])
            node_list.append(node)

        edge_list = list(itertools.combinations(node_list, 2))

        G.add_nodes_from(node_list)
        for e in edge_list:
            G.add_edge(e[0],e[1],weight=1)


    return G

create_seed_network()
