from datetime import datetime
from dateutil.relativedelta import relativedelta

import os.path, sys

import pandas as pd
import numpy as np

import utils

def get_client_owner_gender(file_name, return_name):
    dataframe = pd.read_csv(os.path.abspath('./' + file_name), sep=";", low_memory=False)
    clients = utils.load_dataframe('clients_modified.csv')
    disp = utils.load_dataframe('disp.csv')
    loan_dates = utils.load_dataframe('train_sets/loan_train_modified.csv')[['account_id', 'date']]
    
    owner_clients = disp.groupby(['type'], as_index=False).get_group('OWNER')
    owner_clients = pd.merge(owner_clients, clients, on='client_id', how='outer')
    
    loan_dates = pd.merge(loan_dates, owner_clients, on='account_id', how='left')
    
    ages = []
    genders = []
    
    for index, row in loan_dates.iterrows():
        temp = datetime.strptime(row['birth_date'], '%a, %b %d, \'%y')
        temp_2 = datetime.strptime(row['date'], '%a, %b %d, \'%y')
        client_date = str(temp.day) + "-" + str(temp.month) + "-" + "19" + str(temp.year)[2:]
        loan_date = str(temp_2.day) + "-" + str(temp_2.month) + "-" + "19" + str(temp_2.year)[2:]

        client_date = datetime.strptime(client_date, '%d-%m-%Y')
        loan_date = datetime.strptime(loan_date, '%d-%m-%Y')
        
        client_age = relativedelta(loan_date, client_date).years

        ages.append(client_age)
        
        if row['gender'] == 'male':
            genders.append(0)
        else:
            genders.append(1)
    
    loan_dates['client_age'] = ages
    loan_dates['gender'] = genders
    loan_dates = loan_dates[['account_id', 'gender', 'client_age', 'district_id']]

    dataframe = pd.merge(dataframe, loan_dates, on='account_id', how='outer')
    
    utils.write_dataframe_to_CSV(dataframe, return_name)
        
get_client_owner_gender('dataset_train_v1.csv', 'dataset_train_v1_v3.csv')
get_client_owner_gender('dataset_train_v2.csv', 'dataset_train_v2_v3.csv')