from collections import *
import json
import config
import codecs
import string
from ftfy import fix_encoding
import unicodedata
import cPickle
import pprint


def clean_tweet_token(s):

    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = s.encode('ascii', 'ignore')
    s = s.strip('",;')
    s = string.lower(s)
    return s

def process_json(_dict):
    result = []
    entity_list = []
    entity_fields = ['named_entities_organization',
                     'named_entities_person',
                     'named_entities_product']

    for e in entity_fields:
        instances = _dict[e]
        for i in instances:
            i = clean_tweet_token(i)
            entity_list.append(i)

    text_data = []
    text_fields = ['noun_chunks',
                   'hashtags',
                   'matched_queries',
                   'categories']

    for t in text_fields:
        td = _dict[t]
        for token in td:
            token = clean_tweet_token(token)
            if len(token) > 0:
                text_data.append(token)


    # assuming multiple entities are present!
    for e in entity_list:
        if len(e)> 0 :
            res = {e:text_data}
        result.append(res)

    return result

# Returns a dictionary  { entity : [ <keywords> ] }
def process_tweet_data():

    inp_file_name = config.tweet_data_file
    result = []
    with codecs.open(inp_file_name,'r',encoding='utf8') as fp:
        for line in fp:
            _dict = json.loads(line)
            res = process_json(_dict)
            result.append(res)
    return result


res = process_tweet_data()
with open(config.tweet_data_save_file, "wb") as f:
    cPickle.dump(res, f)

pprint.pprint(res)