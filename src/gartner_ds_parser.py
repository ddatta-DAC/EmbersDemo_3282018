import pandas as pd
import sys
import os

data_file_loc = './../data'
data_file_name = 'gartner_clean.csv'
data_file_path = data_file_loc + '/' + data_file_name

df = pd.read_csv(data_file_path, header = 0 )
print df

