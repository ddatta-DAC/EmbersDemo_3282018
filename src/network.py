import networkx as nx
import gartner_ds_parser as gp
import itertools
import pprint
import cPickle
import config
from entity import entity
import vsm_1

# -------------------------------------------------- #

class entity_network:

    def __init__(self, init=False):
        self.save_file = config.company_network_file
        self.G = None

        if init:
            self.create_network()
        else:
            self.load_model()
        return

    def save_model(self):
        print '> ', self.save_file
        # save the network
        with open(self.save_file, "wb") as f:
            cPickle.dump(self.G, f)
        return

    def load_model(self):
        with open(self.save_file, "rb") as f:
            self.G = cPickle.load(f)
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
                h = str.lower(h)
                if len(h) > 150:
                    continue

                node = entity(h, data['class'])
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

    def get_sim_entities(self, ename):
        sim_com_list = []
        for g in self.G.nodes():
            if g.get_name() == ename:
                # get all neighbors of g
                nbrs = self.G.neighbors(g)
                for n in nbrs:
                    sim_com_list.append(n.get_name())

        return sim_com_list

    def get_node(self, ename):
        for g in self.G.nodes():
            if g.get_name() == ename:
                return g
        return None
    # Input
    # tweet_data = { 'entity' : [ keywords] }
    def enrich(self,tweet_data,vsm_model):

        for entity_name, text in tweet_data.iteritems():
            g = self.get_node(ename=entity_name)
            if g is None:
                g = entity(entity_name)
                self.G.add_nodes_from([g])
                # Todo : add in text data
                # Todo : add in edges


        return


# -------------------------------------------------- #

# -------------------------------------------------- #


# def dummy_test():
#     company_network_obj = company_network(True)
#     company_network_obj.get_network_info()
#     # test_list = ['Facebook', 'ABB', 'NASA', 'Teradata', 'Yahoo', 'Zebra Medical Vision', 'Palantir']
#     # for t in test_list:
#     #     print 'Company :: ', t
#     #     print network_obj.get_sim_companies(t)
#     # print network_obj.get_node('Yahoo').display()
#     # name_list = []
#     # for g in company_network_obj.G.nodes():
#     #     n = g.get_name()
#     #     name_list.append(n)
#     # print name_list
#     # with open('cnames.txt', "w") as f:
#     #     f.write('\n'.join(name_list))
#
# dummy_test()
