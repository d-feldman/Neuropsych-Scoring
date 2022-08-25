################################################################################
## Script to rename all data files 

#You will change:
# os.chdir -- where the data is, and
# sourceFile -- where you want the csv file to go
# path -- path to raw data
################################################################################
import os, sys


# Change These following files
# This is where your data is located
os.chdir('/Users/danielfeldman/Desktop/FEPT_shona/')
  
# This is where you want the participant csv file to be output to
sourceFile = open('/Users/danielfeldman/Desktop/ZEMB_FEPT/SUBJ_List.csv', 'w')

#This is where your data is-- redundancy 
path = "/Users/danielfeldman/Desktop/FEPT_shona"
#################################################################################
###################### This section should not need to be changed ###############
#################################################################################

#Function to rename multiple files
for filename in os.listdir(path):
    file_up = filename.upper()
    f_name, f_ext = os.path.splitext(file_up)
    num = f_name.split('F')
    num_only = num[0]
    f_ext = ".csv"
    new_name = str(num_only) + "_FEPT" + str(f_ext)
    os.rename(filename, new_name)
