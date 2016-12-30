import os.path, sys

import pandas as pd
import numpy as np

from datetime import datetime

import utils

def get_mean_trans_values(file, dataframe):
    trans_mod = utils.load_dataframe(file)
    
    trans_mod.sort_values(by=['date'], ascending=[True])
    
    grouped = trans_mod.groupby(['account_id'], as_index=False)
    
    credits_ = []
    withdrawals_ = []
    balances_ = []
    
    for account_id in dataframe['account_id']:
        withdrawals_month = []
        credits_month = []
        balance_month = []

        current_date = None
        
        withdrawal_amount = 0
        credit_amount = 0
        
        withdrawal_count = 0
        credit_count = 0
        
        sub_group = grouped.get_group(account_id)
        
        for index, trans in sub_group.iterrows():
            date = datetime.strptime(trans['date'], '%a, %b %d, \'%y')
            if current_date is None or current_date == (date.month, date.year):
                current_date = (date.month, date.year)
                if trans['type'] == 'credit':
                    credit_amount = credit_amount + trans['amount']
                    credit_count = credit_count + 1
                elif trans['type'] == 'withdrawal' or trans['type'] == 'withdrawal in cash':
                    withdrawal_amount = withdrawal_amount + trans['amount']
                    withdrawal_count = withdrawal_count + 1
            else:
                current_date = (date.month, date.year)
                if(withdrawal_count != 0):
                    withdrawals_month.append(withdrawal_amount / withdrawal_count)
                    withdrawal_amount = 0
                    withdrawal_count = 0
                else:
                    withdrawals_month.append(0)
                    withdrawal_amount = 0
                    withdrawal_count = 0
                    
                if(credit_count != 0):
                    credits_month.append(credit_amount / credit_count)
                    credit_amount = 0
                    credit_count = 0
                else:
                    credits_month.append(0)
                    credit_amount = 0
                    credit_count = 0
                    
                if trans['type'] == 'credit':
                    credit_amount = credit_amount + trans['amount']
                    credit_count = credit_count + 1
                elif trans['type'] == 'withdrawal' or trans['type'] == 'withdrawal in cash':
                    withdrawal_amount = withdrawal_amount + trans['amount']
                    withdrawal_count = withdrawal_count + 1
        
        if(withdrawal_count != 0):
            withdrawals_month.append(withdrawal_amount / withdrawal_count)
        else:
            withdrawals_month.append(0)
        
        if(credit_count != 0):
            credits_month.append(credit_amount / credit_count)
        else:
            credits_month.append(0)
        
        if(len(withdrawals_month) != 0):
            withdrawals_.append(round(sum(withdrawals_month) / len(withdrawals_month), 2))
        else:
            withdrawals_.append(0)
        if(len(credits_month) != 0):
            credits_.append(round(sum(credits_month) / len(credits_month), 2))
        else:
            credits_.append(0)
            
        balance_month = [round(i - j, 2) for i, j in zip(credits_month, withdrawals_month)]
        balances_.append(round(sum(balance_month) / len(balance_month), 2))
        
        #print credits_month
        #print withdrawals_month
        #print balance_month
        
    dataframe['credits_mean'] = credits_
    dataframe['withdrawals_mean'] = withdrawals_
    dataframe['balances_monthly_2'] = balances_
                
    return dataframe

def get_mean_balance_amount_racio(file, dataframe):
    trans_mod = utils.load_dataframe(file)
    
    trans_mod.sort_values(by=['date'], ascending=[True])
    
    grouped = trans_mod.groupby(['account_id'], as_index=False)
    
    payments_ = []
    balances_ = []
    
    for index, row in dataframe.iterrows():
        payments_.append(row['amount'] / row['duration'])
        
        sub_group = grouped.get_group(int(row['account_id']))
        
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
        
        #print sub_group
        #print balance_per_month
        
        balances_.append(round(sum(balance_per_month) / len(balance_per_month), 2))

    dataframe['average_balance_monthly'] = balances_
    dataframe['payment_monthly'] = payments_

    return dataframe