import os.path, sys

import pandas as pd
import numpy as np

from datetime import datetime

import utils

def calculate_mean_of_operation_type(input_file_name, output_file_name, trans_file):
    trans = utils.load_dataframe(trans_file)
    dataframe = pd.read_csv(os.path.abspath('./' + input_file_name), sep=";", low_memory=False)
    
    trans_groups = trans.groupby(['account_id'], as_index=False)
    
    credits_cash_ = []
    credits_bank_ = []
    credits_interest_ = []

    withdrawals_cash_ = []
    withdrawals_bank_ = []
    withdrawals_cr_ = []
    
    for index, account in dataframe.iterrows():
        account_trans = trans_groups.get_group(account['account_id'])
        credit_cash = [0, 0]
        credit_a_bank = [0, 0]
        credit_interest = [0, 0]

        withdrawal_cr = [0, 0]
        withdrawal_a_bank = [0, 0]
        withdrawal_cash = [0, 0]

        for i, transaction in account_trans.iterrows():
            if transaction['type'] == 'credit':
                if transaction['operation'] == 'collection from another bank':
                    credit_a_bank[0] = credit_a_bank[0] + 1
                    credit_a_bank[1] = credit_a_bank[1] + transaction['amount']
                elif transaction['operation'] == 'credit in cash':
                    credit_cash[0] = credit_cash[0] + 1
                    credit_cash[1] = credit_cash[1] + transaction['amount']
                else:
                    credit_interest[0] = credit_interest[0] + 1
                    credit_interest[1] = credit_interest[1] + transaction['amount']
            elif transaction['type'] == 'withdrawal':
                if transaction['operation'] == 'credit card withdrawal':
                    withdrawal_cr[0] = withdrawal_cr[0] + 1
                    withdrawal_cr[1] = withdrawal_cr[1] + transaction['amount']
                elif transaction['operation'] == 'remittance to another bank':
                    withdrawal_a_bank[0] = withdrawal_a_bank[0] + 1
                    withdrawal_a_bank[1] = withdrawal_a_bank[1] + transaction['amount']
                elif transaction ['operation'] == 'withdrawal in cash':
                    withdrawal_cash[0] = withdrawal_cash[0] + 1
                    withdrawal_cash[1] = withdrawal_cash[1] + transaction['amount']

        if credit_cash[0] == 0:
            credits_cash_.append(0)
        else:
            credits_cash_.append(credit_cash[1] / credit_cash[0])
            
        if credit_a_bank[0] == 0:
            credits_bank_.append(0)
        else:
            credits_bank_.append(credit_a_bank[1] / credit_a_bank[0])
            
        if credit_interest[0] == 0:
            credits_interest_.append(0)
        else:
            credits_interest_.append(credit_interest[1] / credit_interest[0])
            
        if withdrawal_cash[0] == 0:
            withdrawals_cash_.append(0)
        else:
            withdrawals_cash_.append(withdrawal_cash[1] / withdrawal_cash[0])
            
        if withdrawal_cr[0] == 0:
            withdrawals_cr_.append(0)
        else:
            withdrawals_cr_.append(withdrawal_cr[1] / withdrawal_cr[0])
            
        if withdrawal_a_bank[0] == 0:
            withdrawals_bank_.append(0)
        else:
            withdrawals_bank_.append(withdrawal_a_bank[1] / withdrawal_a_bank[0])
        
    dataframe['credits_cash_mean'] = credits_cash_
    dataframe['credits_another_bank_mean'] = credits_bank_
    dataframe['credits_interest_mean'] = credits_interest_
    dataframe['withdrawal_another_bank_mean'] = withdrawals_bank_
    dataframe['withdrawal_cash_mean'] = withdrawals_cash_
    dataframe['withdrawal_credit_card_mean'] = withdrawals_cr_

    utils.write_dataframe_to_CSV(dataframe, output_file_name)

def check_if_account_has_sactions(input_file_name, output_file_name, trans_file):
    trans = utils.load_dataframe(trans_file)
    dataframe = pd.read_csv(os.path.abspath('./' + input_file_name), sep=";", low_memory=False)
    
    trans_groups = trans.groupby(['account_id'], as_index=False)
    
    sanctions_ = []
    
    for index, account in dataframe.iterrows():
        account_trans = trans_groups.get_group(account['account_id'])
        
        sanction = 0
        
        for i, transaction in account_trans.iterrows():
            if transaction['k_symbol'] == 'sanction interest if negative balance':
                sanction = 1
                break
            
        sanctions_.append(sanction)
        
    dataframe['has_sanctions'] = sanctions_

    utils.write_dataframe_to_CSV(dataframe, output_file_name)
    
#calculate_mean_of_operation_type('dataset_train_v2_v4.csv', 'dataset_train_v2_v5.csv', 'train_sets/trans_train.csv')
#calculate_mean_of_operation_type('dataset_test_v2_v4.csv', 'dataset_test_v2_v5.csv', 'test_sets/trans_test.csv')

check_if_account_has_sactions('dataset_train_v2_v5.csv', 'dataset_train_v2_v6.csv', 'train_sets/trans_train.csv')
check_if_account_has_sactions('dataset_test_v2_v5.csv', 'dataset_test_v2_v6.csv', 'test_sets/trans_test.csv')

