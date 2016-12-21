import os.path, sys

import pandas as pd

def load_dataframe(path):
	dataframe = pd.read_csv(os.path.abspath('./../data/' + path), sep=";", low_memory=False)
	return dataframe

def write_dataframe_to_CSV(dataframe, name):
	dataframe.to_csv(os.path.abspath('./../source/' + name), sep=";", index = False)
 
def format_date_in_trans_test_CSV():
    dataframe = load_dataframe('test_sets/trans_test.csv')
    
    from datetime import datetime
    converted_dates = []

    for row in dataframe['date']:
        year = str(row)[:2]
        month = str(row)[2:4]
        day = str(row)[4:6]
        date = "" + day + " " + month + " 19" + year
        converted_dates.append(datetime.strptime(date, "%d %m %Y").strftime('%a, %b %d, \'%y'))

    dataframe['date'] = converted_dates
    dataframe.to_csv(os.path.abspath('./../data/test_sets/trans_test_modified.csv'), sep=";")
    
def format_date_in_trans_train_CSV():
    dataframe = load_dataframe('train_sets/trans_train.csv')
    
    from datetime import datetime
    converted_dates = []

    for row in dataframe['date']:
        year = str(row)[:2]
        month = str(row)[2:4]
        day = str(row)[4:6]
        date = "" + day + " " + month + " 19" + year
        converted_dates.append(datetime.strptime(date, "%d %m %Y").strftime('%a, %b %d, \'%y'))

    dataframe['date'] = converted_dates
    dataframe.to_csv(os.path.abspath('./../data/train_sets/trans_train_modified.csv'), sep=";")
    
format_date_in_trans_train_CSV()