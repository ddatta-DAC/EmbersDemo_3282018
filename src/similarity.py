import gensim
import numpy as np


class pretrained_model:

    def __init__(self):
        self.load_pretrained_model()

    def load_pretrained_model(self):
        model_loc = '../pretrained'
        model_file_name = 'GoogleNews-vectors-negative300.bin'
        model_path = model_loc + '/' + model_file_name
        model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
        self.model = model


    def get_sim_score(self, keyword_list , text_list):
        score = 0
        for k in keyword_list:
            for t in text_list:
                score += self.model.wv.similarity(k,t)
        score = score / len(keyword_list)
        return score
    
    def get_most_sim(self,word):
        try:
            return self.model.wv.most_similar_cosmul([word])
        except :
            print ' nope!'

pt = pretrained_model()
ls = ['facebook','blockchain','iot','spacex','cryptocurrency','Ariba','networks']
for l in ls :
    print '--',l
    print pt.get_most_sim(l)




