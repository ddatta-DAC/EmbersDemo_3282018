import networkx as nx
import gartner_ds_parser as gp
import itertools
import pprint
import cPickle
import config
from entity import entity
import vsm_1
import re
import collections
import util


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

    def create_node(self, name):
        name = self.clean_entity_name(name)
        return entity(name)

    def clean_entity_name(self, e_name):
        return util.clean_entity_name(e_name)

    def save_model(self):
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
        return

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

                node = self.create_node(h)
                # check if node exists!
                for g in self.G.nodes():
                    if g.get_name() == h:
                        node = g
                        break
                node.set_text(text_data=data['text'])
                node_list.append(node)

            edge_list = list(itertools.combinations(node_list, 2))
            self.G.add_nodes_from(node_list)
            for e in edge_list:
                cur_wt = 0
                if self.G.has_edge(e[0], e[1]):
                    # print 'Edge exists : ',e[0].get_name(),'--', e[1].get_name()
                    cur_wt = (self.G.get_edge_data(e[0], e[1]))['weight']

                self.G.add_edge(e[0], e[1], weight=cur_wt + 1)

        self.save_model()
        return

    def get_sim_entities(self, ename):
        sim_com_list = []
        for g in self.G.nodes():
            if g.get_name() == ename:
                # get all neighbors of g
                nbrs = self.G.neighbors(g)

                for n in nbrs:
                    score = self.G.get_edge_data(n, g)
                    scr = score['weight']
                    sim_com_list.append([n.get_name(), scr])

        return sim_com_list

    def get_node(self, ename):
        for g in self.G.nodes():
            if g.get_name() == ename:
                return g
        return None

    # Input
    # tweet_data = { 'entity' : [ keywords] }
    def enrich(self, tweet_data, vsm_model):

        for entity_name, text in tweet_data.iteritems():
            node = self.get_node(ename=entity_name)

            if node is None:
                node = self.create_node(entity_name)
                self.G.add_node(node)
                # print 'Adding to graph', node.get_name()

            # Add in text(tweet) data
            node.set_text(text)
            node.set_tweet_text(text)

        # Add in edges
        self.add_edges_by_tweet(vsm_model)
        self.save_model()
        return

    def add_edges_by_tweet(self, vsm_model):

        all_nodes = self.G.nodes()
        for g in all_nodes:
            # skip if it has no tweet data
            if len(g.get_tweet_text()) == 0:
                continue
            else:
                # get the most similar nodes

                e_name_1 = g.get_name()
                # print '->', e_name_1
                query = g.get_tweet_text()
                ent_score = vsm_model.get_most_sim_entity(target=e_name_1, text_data=query)
                for e_name_2, score in ent_score.iteritems():
                    node = self.get_node(e_name_2)
                    if node is not None and score >= config.score_threshold:
                        cur_wt = 0
                        # print 'Adding [', e_name_2, '--', e_name_1, ']', score
                        if self.G.has_edge(g, node):
                            cur_wt = (self.G.get_edge_data(g, node))['weight']
                        wt = cur_wt + score
                        self.G.add_edge(g, node, weight=wt)

        return

    def get_entity_list(self):
        entity_list = []
        all_nodes = self.G.nodes()
        for g in all_nodes:
            entity_list.append(g.get_name())
        return entity_list


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
#
# company_network_obj = entity_network(False)
# company_network_obj.get_network_info()
# print company_network_obj.get_sim_entities('facebook')
# print company_network_obj.get_node('facebook').display()
