import network
import entity
import vsm_1
import config
import parse_tweet_inputs
import json

# ---------------------- #


def generate_ouput(op_file):

    fp = open(op_file, 'w')
    if  config.tweets_ingestion_done:
        tweet_data = parse_tweet_inputs.load_tweet_data()
    else:
        tweet_data = parse_tweet_inputs.parse_save_tweet_data()

    vsm_model = vsm_1.vsm(input=tweet_data, init=config.tweet_vsm_init)
    entity_graph = network.entity_network(config.gartner_network_init)
    if  config.include_tweets:
        entity_graph.enrich(tweet_data, vsm_model)

    #create test list :
    entity_list = entity_graph.get_entity_list()
    for t in entity_list:
        print 'entity :: ', t
        res = entity_graph.get_sim_entities(t)
        op = { t : res }
        op = json.dumps(op)
        fp.write(op)
        fp.write('\n')

    fp.close()


#---------------#

config.gartner_network_init = True
config.tweet_vsm_init = False
config.tweets_ingestion_done = True
config.include_tweets = False
generate_ouput('seed_op.json')

config.gartner_network_init = False
config.tweet_vsm_init = False
config.tweets_ingestion_done = True
config.include_tweets = True
generate_ouput('seed_tweet_op.json')


