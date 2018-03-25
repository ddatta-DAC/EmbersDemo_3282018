from collections import *
import json
import config
import codecs
import string
import unicodedata
import cPickle
import pprint


def clean_tweet_token(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = s.encode('ascii', 'ignore')
    s = s.strip('",;')
    s = s.strip()
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
        if len(e) > 0:
            res = {e: text_data}
            print ' > > ', res
            result.append(res)

    return result


def format_data(input_list):
    ent_text_dict = {}
    for item in input_list:
        _item = item[0]
        if not isinstance(_item, dict):
            continue
        for ent, text in _item.iteritems():
            if ent not in ent_text_dict.keys():
                ent_text_dict[ent] = text
            else:
                ent_text_dict[ent].extend(text)
    return ent_text_dict


# Returns a dictionary  { entity : [ <keywords> ] }
def process_tweet_data():
    inp_file_name = config.tweet_data_file
    result = []
    with codecs.open(inp_file_name, 'r', encoding='utf8') as fp:
        for line in fp:
            _dict = json.loads(line)
            res = process_json(_dict)
            if res:
                result.append(res)
    pprint.pprint(result)
    result = format_data(result)
    return result


def parse_save_tweet_data():
    res = process_tweet_data()
    pprint.pprint(res)
    with open(config.tweet_data_save_file, "wb") as f:
        cPickle.dump(res, f)


def load_tweet_data():
    with open(config.tweet_data_save_file, "rb") as f:
        tweet_dict = cPickle.load(f)
        return tweet_dict


parse_save_tweet_data()
