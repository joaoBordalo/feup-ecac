from __future__ import division

import os.path, sys

import pandas as pd
import numpy as np

import utils

def get_enterpreneurs_ratio(input_file_name, output_file_name):
    dataframe = pd.read_csv(os.path.abspath('./' + input_file_name), sep=";", low_memory=False)
    districts = utils.load_dataframe('district.csv')
    
    average_salaries = []
    unemployment_rates_96 = []
    enterpreneurs_ratio = []
    
    for index, row in dataframe.iterrows():
        for i, district in districts.iterrows():
            if row['district_id'] == district[0]:
                average_salaries.append(district[10])
                unemployment_rates_96.append(district[12])
                total_number_inhabitants = district[3]
                number_enterpreneurs = district[13]
                enterpreneur_probability = (number_enterpreneurs * (total_number_inhabitants / 1000)) / total_number_inhabitants
                enterpreneurs_ratio.append(enterpreneur_probability)
                break
                
    dataframe['district_average_salary'] = average_salaries
    dataframe['district_unemployment_rate'] = unemployment_rates_96
    dataframe['enterpreneur_ratio'] = enterpreneurs_ratio
    
    utils.write_dataframe_to_CSV(dataframe, output_file_name)
    
get_enterpreneurs_ratio('dataset_train_v1_v3.csv', 'dataset_train_v1_v4.csv')
get_enterpreneurs_ratio('dataset_train_v2_v3.csv', 'dataset_train_v2_v4.csv')
get_enterpreneurs_ratio('dataset_test_v1_v3.csv', 'dataset_test_v1_v4.csv')
get_enterpreneurs_ratio('dataset_test_v2_v3.csv', 'dataset_test_v2_v4.csv')