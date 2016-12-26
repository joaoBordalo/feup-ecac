from __future__ import division

import os.path, sys

import pandas as pd
import numpy as np

def classify_clusters(file_name, return_name):
    clusters_dataframe = pd.read_csv(os.path.abspath('./clustering/' + file_name), sep=";", low_memory=False)
    
    clusters = clusters_dataframe.groupby(['cluster'], as_index=False)
    
    result = pd.DataFrame(columns=['Cluster', 'Loan Successfull', 'Loan Unsuccessfull'])
    
    cluster_column = []
    loan_succ_column = []
    loan_unsucc_column = []
    
    for name, group in clusters:
        positives = 0
        negatives = 0
        
        cluster_column.append(name)
        
        for index, row in group.iterrows():
            if row['status'] == 1:
                positives = positives + 1
            else:
                negatives = negatives + 1
                
        loan_succ_column.append(round(positives / len(group), 3))
        loan_unsucc_column.append(round(negatives / len(group), 3))

    print loan_succ_column
    
    result['Cluster'] = cluster_column
    result['Loan Successfull'] = loan_succ_column
    result['Loan Unsuccessfull'] = loan_unsucc_column

    print result

    result.to_csv(os.path.abspath('./clustering/' + return_name), sep=";", index = False)

#classify_clusters('1st_clustering/clustering_v1.csv', '1st_clustering/clustering_v1_results.csv')
#classify_clusters('2nd_clustering/clustering_v2.csv', '2nd_clustering/clustering_v2_results.csv')
#classify_clusters('3rd_clustering/clustering_v3_amount_dur.csv', '3rd_clustering/clustering_v3_amount_dur_results.csv')
classify_clusters('4th_clustering/4th_clustering.csv', '4th_clustering/4th_clustering_results.csv')
