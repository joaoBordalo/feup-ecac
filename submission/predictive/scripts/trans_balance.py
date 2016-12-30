import os.path, sys

import pandas as pd
import numpy as np

import utils

from datetime import datetime

def get_last_balance(file_trans, file_dataset):
    trans_mod = utils.load_dataframe(file_trans)
    dataframe = pd.read_csv(os.path.abspath('./' + file_dataset), sep=";", low_memory=False)
    
    trans_mod.sort_values(by=['date'], ascending=[True])
    
    grouped = trans_mod.groupby(['account_id'], as_index=False)
    
    balances = []
    
    for row in dataframe['account_id']:
        balances.append(round(grouped.get_group(row)['balance'].iloc[-1], 2))
            
    dataframe['last_balance'] = balances
   
    utils.write_dataframe_to_CSV(dataframe, file_dataset)
    
    
get_last_balance('train_sets/trans_train_modified.csv', 'dataset_train_v2_v3.csv')
get_last_balance('test_sets/trans_test_modified.csv', 'dataset_test_v2_v3.csv')