import os.path, sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import utils
import clustering
import trans_train

def create_basic_dataframe(dataframe):
	df = pd.DataFrame()

	df['account_id'] = dataframe['account_id']
	df['duration'] = dataframe['duration']
	df['amount'] = dataframe['amount']

	return df

def create_status_dataframe(dataframe):
    df = pd.DataFrame()
    df['status'] = dataframe['status']
    
    return df
    
#################################### Train Files #########################################
#==============================================================================
# # loading loan train file
# loans_mod = utils.load_dataframe('train_sets/loan_train_modified.csv')
# # create simple dataset
# basic_v1 = create_basic_dataframe(loans_mod)
# basic_v1.drop(basic_v1.columns[0], axis=1)
# utils.write_dataframe_to_CSV(basic_v1, 'dataset_train_v1.csv')
# # calculate the mean of transactions
# basic_v2 = trans_train.get_mean_trans_values('train_sets/trans_train_modified.csv', basic_v1)
# basic_v2 = trans_train.get_mean_balance_amount_racio('train_sets/trans_train_modified.csv', basic_v2)
# utils.write_dataframe_to_CSV(basic_v2, 'dataset_train_v2.csv')
#==============================================================================

#################################### Test Files #########################################
#utils.format_date_in_trans_test_CSV()
loans_test_mod= utils.load_dataframe('test_sets/loan_test_modified.csv')
test_v1 = create_basic_dataframe(loans_test_mod)
test_v1.drop(test_v1.columns[0], axis=1)
utils.write_dataframe_to_CSV(test_v1, 'dataset_test_v1.csv')

test_v2 = trans_train.get_mean_trans_values('test_sets/trans_test_modified.csv', test_v1)
test_v2 = trans_train.get_mean_balance_amount_racio('test_sets/trans_test_modified.csv', test_v2)
utils.write_dataframe_to_CSV(test_v2, 'dataset_test_v2.csv')

#########################################################################################

#basic_v1 clustering
#==============================================================================
# model_v1 = clustering.build_model(5)
# model_v1.fit(basic_v1)
# 
# # View the results
# # Set the size of the plot
# plt.figure(figsize=(20,7))
#  
# # Create a colormap
# colormap = np.array(['red', 'blue', 'yellow', 'pink', 'green'])
#  
# # Plot the Models Classifications
# plt.subplot(1, 2, 2)
# plt.scatter(basic_v1.duration, basic_v1.amount, c=colormap[model_v1.labels_], s=40)
# plt.title('K Mean Classification V1')
#==============================================================================

#########################################################################################
