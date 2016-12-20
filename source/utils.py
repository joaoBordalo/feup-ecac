import os.path, sys

import pandas as pd

def load_dataframe(path):
	dataframe = pd.read_csv(os.path.abspath('./../data/' + path), sep=";", low_memory=False)
	return dataframe

def write_dataframe_to_CSV(dataframe, name):
	dataframe.to_csv(os.path.abspath('./../source/' + name), sep=";", index = False)