#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#######################################################################################
###Combine outputs
#######################################################################################
#######################################################################################

import os
import pandas as pd
import csv

#######################################################################################
#Please Make edits to the specifications listed below as indicated by the instructions
#If unsure how to proceed, please contact the MEND2 Lab
#######################################################################################


# This is the path to where all the data you want to combine is located
os.chdir('/Users/danielfeldman/Desktop/PGNGS_20221108/scored')

# This is the NAME of the combined csv file and where you want it to be saved to 
csv_output_name = '/Users/danielfeldman/Desktop/PGNGS_20221108/combined_scored.csv'


####################################################################################
########             DO NOT EDIT ANYTHING BELOW THIS LINE                  #########
####################################################################################

## Combine all files
comb_data = pd.DataFrame()
for filename in os.listdir():
    ind_data = pd.read_csv(filename, header=0, sep=",")
    if comb_data.empty:
        comb_data = ind_data
    else:
        comb_data = comb_data.append(ind_data)
        
comb_data_sort = comb_data.sort_values(by=['user_id'])

## Save combined data
comb_data_sort.to_csv(csv_output_name, index=False)

