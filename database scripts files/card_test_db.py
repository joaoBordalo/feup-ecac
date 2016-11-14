import pandas as pd
import numpy as np
import matplotlib as plt


#read line each line in csv file
df = pd.read_csv('card_test.csv')

#print table
print(df)

print('\n\t Descritive values\n')
# get some descritive numeric values from csv file
print(df.describe())

df['issued'].hist(bins=50)



#
#with open('card_test.csv', newline='') as card_test_file:
#	reader = csv.reader(card_test_file, delimiter =',' )
#	for row in reader:
#		print(row)