from collections import *
import json
import config

def process_json(_dict):
    result = []
    entity_list = []
    entity_fields = ['named_entities_org','named_entities_person','named_entities_product']
    for e in entity_fields:
        instances = _dict[e]
        for i in instances:
            entity_list.append(str(i))
    text_data = []
    text_fields = ['queries','hashtags']

    for t in text_fields:
        td = _dict[t]
        for token in td:
            text_data.append(str(token))

    # assuming multiple entities are present!
    for e in entity_list:
        res = {e:text_data}
        result.append(res)

    return result

# Returns a dictionary  { entity : [ <keywords> ] }
def process_tweet_data():

    inp_file_name = config.tweet_data_file
    result = []
    with open(inp_file_name,'r') as fp:
        l = fp.readline()
        _dict = json.loads(l)
        res = process_json(_dict)
        result.append(res)

    return result



