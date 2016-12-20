import os.path, sys

import pandas as pd
import numpy as np

from datetime import datetime

import utils

def get_mean_trans_values(file, dataframe):
    trans_mod = utils.load_dataframe(file)
    grouped = trans_mod.groupby(['account_id'], as_index=False)
    
    credits_ = []
    withdrawals_ = []
    
    for account_id in dataframe['account_id']:
        withdrawal_amount = 0
        credit_amount = 0
        withdrawal_cash_amount = 0
        
        withdrawal_count = 0
        credit_count = 0
        withdrawal_cash_count = 0
        
        sub_group = grouped.get_group(account_id)
        
        for index, row in sub_group.iterrows():
            if row['type'] == 'credit':
                credit_amount = credit_amount + row['amount']
                credit_count = credit_count + 1
            elif row['type'] == 'withdrawal':
                withdrawal_amount = withdrawal_amount + row['amount']
                withdrawal_count = withdrawal_count + 1
            elif row['type'] == 'withdrawal in cash':
                withdrawal_cash_amount = withdrawal_cash_amount + row['amount']
                withdrawal_cash_count = withdrawal_cash_count + 1

        # append the credit value
        if credit_count == 0:
            credits_.append(0)
        else:
            credits_.append(credit_amount / credit_count)
        
        # append the withdrawal value
        total_withdrawals = withdrawal_amount + withdrawal_cash_amount
        total_withdrawals_count = withdrawal_count + withdrawal_cash_count
        
        if total_withdrawals_count == 0:
            withdrawals_.append(0)
        else:
            withdrawals_.append(total_withdrawals / total_withdrawals_count)
            
    dataframe['credits_mean'] = credits_
    dataframe['withdrawals_mean'] = withdrawals_
                
    return dataframe

def get_mean_balance_amount_racio(file, dataframe):
    trans_mod = utils.load_dataframe(file)
    grouped = trans_mod.groupby(['account_id'], as_index=False)
    
    payments = []
    
    for index, row in dataframe.iterrows():
        payments.append(row['amount'] / row['duration'])
        
        sub_group = grouped.get_group(row['account_id'])
        
        balance_per_month = []
        current_date = None
        balance_idx = 0
        
        for index, trans in sub_group.iterrows():
            date = datetime.strptime(trans['date'], '%a, %b %d, \'%y')
            if current_date is None:
                current_date = (date.month, date.year)
                balance_per_month.append(trans['balance'])
            elif current_date == (date.month, date.year):
                balance_per_month[balance_idx] = trans['balance']
            else:
                current_date = (date.month, date.year)
                balance_idx = balance_idx + 1
                balance_per_month.append(trans['balance'])
        
        print sub_group
        print balance_per_month

        break