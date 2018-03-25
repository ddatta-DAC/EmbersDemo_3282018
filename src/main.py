import network
import entity
import vsm_1
import config
import parse_tweet_inputs


tweet_data = parse_tweet_inputs.load_tweet_data()
vsm_model = vsm_1.vsm(input=tweet_data,init=config.tweet_vsm_init)

network = network.entity_network(config.gartner_network_init)
network.enrich(tweet_data,vsm_model)