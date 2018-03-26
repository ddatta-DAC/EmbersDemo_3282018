import gartner_ds_parser as gp
import pprint
import json

fp = open('gartner_json.json','w')
for i in  gp.gen_data_to_feed():
    print pprint.pprint(i)
    r = json.dumps(i)
    fp.write(r)
    fp.write('\n')

fp.close()
