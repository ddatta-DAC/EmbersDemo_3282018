import cPickle
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import *
from sklearn.metrics.pairwise import linear_kernel
import config
import operator


# ------------------------- #

class vsm:

    # input should be a dictionary
    # { entity_name : [ keywords ] }
    # if init is False, load previosuly saved model
    def __init__(self, input=None, init=True):
        self.save_file = config.vsm_model_file
        self.top_k = config.vsm_top_k
        self.class_dict = {}

        if init == True:
            self.build(input)
            self.save_model()
        else:
            self.load_model()
        return

    def build(self, input_dict):
        corpus = []
        entity_id_dict = {}
        id = 0

        # create corpus
        for k, v in input_dict.iteritems():
            entity_id_dict[k] = id
            id += 1
            corpus.append(' '.join(v))

        self.tf_idf = TfidfVectorizer(analyzer='word',
                                      ngram_range=(1, 1),
                                      min_df=0,
                                      stop_words='english')
        self.tf_idf_matrix = self.tf_idf.fit_transform(corpus)

        print '--- Building vector space model ---'
        feature_names = self.tf_idf.get_feature_names()
        print 'Number of words in the vocab ', len(feature_names)
        print 'tf - idf matrix', self.tf_idf_matrix
        print '---'

        self.entity_tf_idf = {}
        for k, v in entity_id_dict.iteritems():
            row_num = v
            self.entity_tf_idf[k] = self.tf_idf_matrix[row_num:row_num + 1]

        self.class_dict = {
            'tf_idf': self.tf_idf,
            'tf_idf_matrix': self.tf_idf_matrix,
            'entity_tf_idf': self.entity_tf_idf
        }

        return

    def save_model(self):

        with open(self.save_file, "wb") as f:
            cPickle.dump(self.class_dict, f)
        return

    def load_model(self):
        with open(self.save_file, "rb") as f:
            self.class_dict = cPickle.load(f)
        try:
            self.tf_idf = self.class_dict['tf_idf']
            self.tf_idf_matrix = self.class_dict['tf_idf_matrix']
            self.entity_tf_idf = self.class_dict['entity_tf_idf']
        except:
            print ' Error loading vsm model!! '
            exit(1)

        return

    # Input :
    # target <str>
    # text_data : <str>
    # Returns
    # { sim_ent_1 : score , .... }
    def get_most_sim_entity(self, target, text_data):
        response = self.tf_idf.transform([text_data])
        score_dict = {}
        for entity, tf_idf_vector in self.entity_tf_idf.iteritems():
            # Check self-compares
            if target == entity:
                continue
            cos_sim = linear_kernel(response, tf_idf_vector).flatten()
            score_dict[entity] = cos_sim
        # sort
        score_list = sorted(score_dict.items(), key=operator.itemgetter(0))
        # return top k
        top_k = score_list[:self.top_k]
        res = OrderedDict()
        for z in top_k:
            res[z[0]] = z[1][0]
        return res


def test():
    inp = {
        'Trump': ['president', 'motherfucker', 'Ivanka'],
        'Mueller': ['Trump', 'FBI', 'USA'],
        'Adam Levine': ['USA', 'singer', 'music'],
        'Floyd': ['USA', 'Virginia', 'music'],
        'Stallone': ['USA', 'philly', 'music']
    }

    obj = vsm(None, False)
    print obj.get_most_sim_entity('U2', 'USA music band')
    return
