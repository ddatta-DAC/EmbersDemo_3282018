import gensim
import numpy as np


def load_pretrained_model():
    model_loc = '../pretrained'
    model_file_name = 'GoogleNews-vectors-negative300.bin'
    model_path = model_loc + '/' + model_file_name
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    return model

model =load_pretrained_model()

print model.get_vector('godzilla')




