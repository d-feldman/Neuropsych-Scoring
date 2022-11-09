#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#######################################################################################
#######################################################################################
# PGNGS Scoring Script/Function for Pavlovia Keyboard Data       
# Based on code from Summer Frandsen                            
# Adapted, modified logic by Daniel Feldman
#For UIC specific-project
##last edited 11/09/2022
#######################################################################################
#######################################################################################

def PGNGS_PAVK_scoring_func_Natania(sub_id, out_dir, data_dir):

#######################################################################################
#Please Make edits to the specifications listed below as indicated by the instructions
#If unsure how to proceed, please contact the MEND2 Lab
#######################################################################################
    ## These parameters are based on how you set up your PGNGS experience. If unsure, most of these
    ## can be found by looking at some of your output data.
    
    # Which blocks you have -- Put 'yes' or 'no'. *Note that responses are all lowercase
    go_2T = 'yes'
    gng_2T = 'yes'
    gs_2T = 'yes'
   

    # The label of your stimuli target names (eg. "L_diamond.bmp", "L_r.bmp", "L_x.bmp", 'x', 'y')
    t1 = "x"
    t2 = "y"


    # The label of your stop stimuli
    st = "Stop"

    # What your correct response is labeled (ex. 'n', 'space')
    cr = 'n'

    # The set timing of Stimuli (ex. .600, .700, .750)
    iti = .600

############################################################################################
############################################################################################
                    #DO NOT MAKE ANY CHANGES BEYOND THIS POINT
############################################################################################
############################################################################################


#############################
#          SETUP            #
#############################

    #importing necessary packages
    import numpy as np
    import pandas as pd
    import csv
    import re
    import sys

    #Read in data
    PGNGS_data = pd.read_csv((str(data_dir) + '/' + str(sub_id) + '_PGNGS_PAVK.csv'), header=0, sep=',') 

    part_id = sub_id

    #Create Scoring Dataframes
    PGNGS_scores = pd.DataFrame(np.zeros((1,1)), columns=['user_id'])

    PGNGS_scores['user_id'] = part_id

    PGNGS_clean = pd.DataFrame()
    
    PGNGS_ind_scores = pd.DataFrame(np.zeros((1,1)), columns=['user_id'])
    PGNGS_ind_scores['user_id'] = part_id

################################
#   Go Condition - 2 Target    # 
################################

    if go_2T == 'yes':
        #Pull letters into separate dataframe
        mask = np.invert(PGNGS_data.loc[:,'block1_resp.corr'].isna())
        block1_s = PGNGS_data.loc[mask,['stimuli_1', 'block1_resp.keys', 'corrAns1', 'block1_resp.corr', 'block1_resp.rt']]
        block1_s = block1_s.reset_index(drop=True)

        block1_c = block1_s
        PGNGS_clean = pd.concat([PGNGS_clean, block1_c], axis = 1)

        #Set the different scores = to 0
        b1_cor = 0
        b1_omm = 0
        b1_cor_rt = 0
        b1_cor_sd = 0

        #Set a column 
        conditions = [
            (block1_s['stimuli_1'] == t1),
            (block1_s['stimuli_1'] == t2),
            (block1_s['stimuli_1'] != t1) & (block1_s['stimuli_1'] != t2)
            ]

        # create a list of the values we want to assign for each condition
        values = ['G', 'G', 'N']

        # create a new column and use np.select to assign values to it using our lists as arguments
        block1_s['target'] = np.select(conditions, values)


        ### Computing Scores
        #Set empty response time dataframe
        block1_rt = pd.DataFrame()

        for i, row in block1_s.iterrows():

            #If it is a go target
            if row['target'] == 'G':
                #Correct response Score
                #If right on target
                if block1_s.loc[i, 'block1_resp.keys'] == cr: 
                    b1_cor = b1_cor + 1
                    #Save response times
                    block1_rt.loc[i, 'block1c_rt'] = (block1_s.loc[i, 'block1_resp.rt'])
                #If right one after target
                elif block1_s.loc[i + 1, 'block1_resp.keys'] == cr:
                    b1_cor = b1_cor + 1
                    #Save response times
                    block1_rt.loc[i, 'block1c_rt'] = iti + block1_s.loc[i+ 1, 'block1_resp.rt']
                #Ommission score (do not respond at target or one after target)
                elif row['block1_resp.keys'] != 'n' and block1_s.loc[i + 1, 'block1_resp.keys'] != 'n':
                    b1_omm = b1_omm + 1
            else:
                continue

        #Create total Random Response
        b = (block1_s['block1_resp.keys'] == 'n').sum()
        b1_rand_resp = b - b1_cor

        #Create Response time scores
        try:
            b1_cor_rt = block1_rt["block1c_rt"].mean()
        except:
            b1_cor_rt = 0
            print("Error with 2G Go Block mean")

        try:
            b1_cor_sd = block1_rt["block1c_rt"].std()
            if len(block1_rt["block1c_rt"]) <= 1:
                b1_cor_sd = 0 
        except:
            b1_cor_sd = 0
            print("Error with 2G Go Block SD")

        #Create Percent correct
        pc = (block1_s.target == 'G').sum()
        b1_per_cor = b1_cor/pc


        #Check to see if participant responded too many times and num of responsess
        b1_sum = (block1_s['block1_resp.keys'] == 'n').sum()
        b1_tot = (block1_s.corrAns1 == 'n').sum() 
        if b1_sum > (b1_tot + 5):
            print("Participant", "has too many responses in 2T Go Block")
            
        ###Saving responses to scoring dataframe
        PGNGS_scores['2T_go_hit'] = b1_cor
        PGNGS_scores['2T_go_omm'] = b1_omm

        PGNGS_scores['2T_go_rand_com'] = b1_rand_resp

        PGNGS_scores['2T_go_rt'] = b1_cor_rt
        PGNGS_scores['2T_go_sd'] = b1_cor_sd

        PGNGS_scores['2T_per_cor'] = b1_per_cor

################################
#   GNG Condition - 2 Target   # 
################################

    if gng_2T == 'yes':
        #Pull letters into separate dataframe
        mask = np.invert(PGNGS_data.loc[:,'block2_resp.corr'].isna())
        block2_s = PGNGS_data.loc[mask,['stimuli_2', 'block2_resp.keys', 'corrAns2', 'block2_resp.corr', 'block2_resp.rt']]
        block2_s = block2_s.reset_index(drop=True)

        block2_c = block2_s
        PGNGS_clean = pd.concat([PGNGS_clean, block2_c], axis = 1)
        
        ind_scores_2T_ng = pd.DataFrame()

        #Set the different scores = to 0
        b2_cor = 0
        b2_omm = 0
        b2_comm = 0
        b2_rej = 0
        b2_miss_opp = 0 
        b2_miss_op_sub = 0 

        #Set a column 
        conditions = [
            (block2_s['stimuli_2'] == t1),
            (block2_s['stimuli_2'] == t2),
            (block2_s['stimuli_2'] != t1) & (block2_s['stimuli_2'] != t2)
            ]

        # create a list of the values we want to assign for each condition
        values = [1, 2, 0]

        # create a new column and use np.select to assign values to it using our lists as arguments
        block2_s['stim_type'] = np.select(conditions, values)

        #Clarify Go and Lure conditions
        t = ''
        l = ''

        for a, type in block2_s.iterrows():
            if type['stim_type'] == 1:
                if t == 'd1' and l == 'n':
                    block2_s.loc[a, 'target'] = 'L'
                    l = 'y'
                    t = 'd1'
                elif t == 'd1' and l == 'y':
                    block2_s.loc[a, 'target'] = 'O'
                    l = 'y'
                    t = 'd1'
                else:
                    block2_s.loc[a, 'target'] = 'G'
                    l = 'n'
                    t = 'd1'
            elif type ['stim_type'] == 2:
                if t == 'd2' and l == 'n':
                    block2_s.loc[a, 'target'] = 'L'
                    l = 'y'
                    t = 'd2'
                elif t == 'd2' and l == 'y':
                    block2_s.loc[a, 'target'] = 'O'
                    l = 'y'
                    t = 'd2'
                else:
                    block2_s.loc[a, 'target'] = 'G'
                    l = 'n'
                    t = 'd2'
            else: 
                block2_s.loc[a, 'target'] = 'N'

        ####Create Scores
        block2cor_rt = pd.DataFrame()
        block2com_rt = pd.DataFrame()
        for d, row in block2_s.iterrows():
            #If row is a Go target
            if row['target'] == 'G':
                #If they respond
                if block2_s.loc[d, 'block2_resp.keys'] == cr:
                    block2_s.loc[d, 'miss_opp'] = 0
                    hold = d
                    b2_cor = b2_cor + 1
                    block2cor_rt.loc[d, 'block2cr_rt'] = block2_s.loc[d, 'block2_resp.rt']
                #If they respond one stimuli after
                elif block2_s.loc[d + 1, 'block2_resp.keys'] == cr:
                    block2_s.loc[d, 'miss_opp'] = 0
                    hold = d
                    b2_cor = b2_cor + 1
                    block2cor_rt.loc[d, 'block2cr_rt'] = iti + block2_s.loc[d + 1, 'block2_resp.rt']

                #If they don't respond
                else:
                    block2_s.loc[d, 'miss_opp'] = 1
                    hold = d
                    b2_omm = b2_omm + 1

            #If row is a lure        
            elif row['target'] == 'L':
                #If they respond
                if block2_s.loc[d, 'block2_resp.keys'] == cr:
                    #If they did not miss the go target before
                    if block2_s.loc[hold, 'miss_opp'] == 0:
                        block2_s.loc[d, 'lure_corr'] = 0
                        block2_s.loc[d, 'miss_opp'] = 0
                        b2_comm = b2_comm + 1
                        block2com_rt.loc[d, 'block2cm_rt'] = block2_s.loc[d, 'block2_resp.rt']
                    #If they missed the go target before
                    else: 
                        block2_s.loc[d, 'miss_opp'] = 1
                        block2_s.loc[d, 'lure_corr'] = 0
                        b2_miss_opp = b2_miss_opp + 1
                        b2_miss_op_sub = b2_miss_op_sub + 1
                #If they respond one stimiuli late        
                elif block2_s.loc[d + 1, 'block2_resp.keys'] == cr:
                    if block2_s.loc[hold, 'miss_opp'] == 0:
                        block2_s.loc[d, 'lure_corr'] = 0
                        block2_s.loc[d, 'miss_opp'] = 0
                        b2_comm = b2_comm + 1
                        block2com_rt.loc[d, 'block2cm_rt'] = iti + block2_s.loc[d + 1, 'block2_resp.rt']
                    else: 
                        block2_s.loc[d, 'miss_opp'] = 1
                        block2_s.loc[d, 'lure_corr'] = 0
                        b2_miss_opp = b2_miss_opp + 1
                        b2_miss_op_sub = b2_miss_op_sub + 1

                elif block2_s.loc[d, 'block2_resp.keys'] != 'n' and block2_s.loc[d + 1, 'block2_resp.keys'] != 'n':
                    if block2_s.loc[hold, 'miss_opp'] == 0:
                        block2_s.loc[d, 'lure_corr'] = 1
                        block2_s.loc[d, 'miss_opp'] = 0
                        b2_rej = b2_rej + 1
                    else:
                        block2_s.loc[d, 'miss_opp'] = 1
                        block2_s.loc[d, 'lure_corr'] = 1
                        b2_miss_opp = b2_miss_opp + 1
                else:
                    print('error in Go/No-Go line', d)

        #Total Random Score:
        b = (block2_s['block2_resp.keys'] == 'n').sum()
        b2_rand_resp = b - (b2_cor + b2_comm + b2_miss_op_sub) 

        #Create Response time scores
        try:
            b2_cor_rt = block2cor_rt["block2cr_rt"].mean()
        except:
            b2_cor_rt = 0
            print("Error with 2T GNG Block correct mean")

        try:
            b2_cor_sd = block2cor_rt["block2cr_rt"].std()
            if len(block2cor_rt["block2cr_rt"]) <= 1:
                b2_cor_sd = 0 
        except:
            b2_cor_sd = 0
            print("Error with 2T GNG Block correct sd")

        try:
            b2_com_rt = block2com_rt["block2cm_rt"].mean()
        except:
            b2_com_rt = 0
            print("Error with 2T GNG Block commision mean")

        try:
            b2_com_sd = block2com_rt["block2cm_rt"].std()
            if len(block2com_rt["block2cm_rt"]) <= 1:
                b2_com_sd = 0
        except:
            b2_com_sd = 0
            print("Error with 2T GNG Block commission sd")

        #Create Percent correct
        pc_g = (block2_s.target == 'G').sum()
        b2_per_cor_g = b2_cor/pc_g               

        pc_l = (block2_s.target == 'L').sum()
        b2_per_cor_l = b2_rej/pc_l


        #Check to see if participant responded too many times and num of responses
        b2_sum = (block2_s['block2_resp.keys'] == 'n').sum()
        b2_tot = (block2_s.corrAns2 == 'n').sum() 
        if b2_sum > (b2_tot + b2_comm + 5):
            print("Participant", "has too many responses in 2T GNG Block")

        if b2_rej <= 1:
            print("Participant has 1 or less correct rejections in 2T GNG Block")
        
        #Creating Individual Scored Data
        mask = block2_s.loc[:,'target'] == 'L'
        ind_scores_2T_ng['2T_ng_cor']= pd.Series([block2_s.loc[mask,['lure_corr']]])
        ind_scores_2T_ng['T_ng_mo']= block2_s.loc[mask,['miss_opp']]
        ind_scores_2T_ng = ind_scores_2T_ng.reset_index(drop=True)

        PGNGS_ind_scores = pd.concat([PGNGS_ind_scores,ind_scores_2T_ng], axis=1)

        ###Save Scores to scoring dataframe
        PGNGS_scores['2T_gng_hit'] = b2_cor
        PGNGS_scores['2T_gng_omm'] = b2_omm
        PGNGS_scores['2T_gng_comm'] = b2_comm
        PGNGS_scores['2T_gng_reject'] = b2_rej
        PGNGS_scores['2T_gng_missopp'] = b2_miss_opp

        PGNGS_scores['2T_gng_rand_com'] = b2_rand_resp

        PGNGS_scores['2T_gng_cor_rt'] = b2_cor_rt
        PGNGS_scores['2T_gng_cor_sd'] = b2_cor_sd

        PGNGS_scores['2T_gng_com_rt'] = b2_com_rt
        PGNGS_scores['2T_gng_com_sd'] = b2_com_sd

        PGNGS_scores['2T_gng_cor_per_g'] = b2_per_cor_g
        PGNGS_scores['2T_gng_cor_per_l'] = b2_per_cor_l

################################
# Go/Stop Condition - 2 Target # 
################################

    if gs_2T == 'yes':
        mask = np.invert(PGNGS_data.loc[:,'block3_resp.corr'].isna())
        block3_s = PGNGS_data.loc[mask,['stimuli_3', 'block3_resp.keys', 'stimuli_3s', 'corrAns3', 'block3_resp.corr', 'block3_resp.rt', 'time_3']]
        block3_s['time_3'] = block3_s['time_3'].astype(float)
        block3_s = block3_s.reset_index(drop=True)

        block3_c = block3_s
        PGNGS_clean = pd.concat([PGNGS_clean, block3_c], axis = 1)
        
        ind_scores_2T_gs = pd.DataFrame() 

        #Set all scores = to 0
        b3_cor = 0
        b3_omm = 0
        b3_comm = 0
        b3_rej = 0
        b3_stoptime = 0
        b3_fstoptime = 0

        ###Clarify Go/Stop Conditions
        conditions = [
            (block3_s['stimuli_3'] == t1),
            (block3_s['stimuli_3'] == t2),
            (block3_s['stimuli_3'] != t1) & (block3_s['stimuli_3'] != t2)
            ]

        # create a list of the values we want to assign for each condition
        values = ['G', 'G', 'N']

        # create a new column and use np.select to assign values to it using our lists as arguments
        block3_s['target'] = np.select(conditions, values)

        for i, row in block3_s.iterrows():
            if row['stimuli_3s'] == st:
                block3_s.loc[i-1, 'target'] = 'S'
            else:
                continue 

        ### Compute Scores
        block3cor_rt = pd.DataFrame()
        block3com_rt = pd.DataFrame()
        block3f_stp = pd.DataFrame()
        block3cor_stp = pd.DataFrame()

        for i, row in block3_s.iterrows():
            if row['target'] == 'G':
                #make sure not following a stop#
                if block3_s.loc[i-1, 'target'] != 'S':
                    #correct in event and one event after
                    if block3_s.loc[i, 'block3_resp.keys'] == cr:
                        b3_cor = b3_cor + 1
                        block3cor_rt.loc[i, 'block3cr_rt'] = block3_s.loc[i, 'block3_resp.rt']
                    elif block3_s.loc[i + 1, 'block3_resp.keys'] == cr:
                        b3_cor = b3_cor + 1
                        block3cor_rt.loc[i, 'block3cr_rt'] = iti + block3_s.loc[i+1, 'block3_resp.rt']
                    #Ommission 
                    elif block3_s.loc[i, 'block3_resp.keys'] !=  'n' and block3_s.loc[i+1, 'block3_resp.keys'] !=  'n':
                        b3_omm = b3_omm + 1
                    else:
                        continue
                #commission (letter time + stop time + additional time -- anytime within 3 of next letter)
            elif row['target'] == 'S':
                #Correct Rejections
                if block3_s.loc[i, 'block3_resp.keys'] != 'n' and block3_s.loc[i + 1, 'block3_resp.keys'] != 'n':
                    block3_s.loc[i, 'stop_corr'] = 1
                    b3_rej = b3_rej + 1
                    block3cor_stp.loc[i, 'block3stp_time_cr'] = block3_s.loc[i, 'time_3']
                #Commisions
                elif block3_s.loc[i, 'block3_resp.keys'] == cr: 
                    block3_s.loc[i, 'stop_corr'] = 0
                    b3_comm = b3_comm + 1
                    block3f_stp.loc[i, 'block3stp_time_fail'] = block3_s.loc[i, 'time_3']
                    block3com_rt.loc[i, 'block3cm_rt'] = block3_s.loc[i, 'block3_resp.rt']
                elif block3_s.loc[i + 1, 'block3_resp.keys'] == cr:
                    block3_s.loc[i, 'stop_corr'] = 0
                    b3_comm = b3_comm + 1
                    block3f_stp.loc[i, 'block3stp_time_fail'] = block3_s.loc[i, 'time_3']
                    block3com_rt.loc[i, 'block3cm_rt'] = block3_s.loc[i, 'time_3'] + block3_s.loc[i+1, 'block3_resp.rt']
                elif block3_s.loc[i + 2, 'block3_resp.keys'] == cr:
                    block3_s.loc[i, 'stop_corr'] = 0
                    b3_comm = b3_comm + 1
                    block3f_stp.loc[i, 'block3stp_time_fail'] = block3_s.loc[i, 'time_3']
                    block3com_rt.loc[i, 'block3cm_rt'] = block3_s.loc[i, 'time_3'] + block3_s.loc[i+1, 'time_3'] + block3_s.loc[i+2, 'block3_resp.rt']

                else:
                    continue

        #Total Random Responses
        b = (block3_s['block3_resp.keys'] == 'n').sum()
        b3_rand_resp = b - (b3_cor + b3_comm)

        #Create Response time scores
        try:
            b3_cor_rt = block3cor_rt['block3cr_rt'].mean()
        except:
            b3_cor_rt = 0
            print("Error with 2G GS Block correct mean")

        try:
            b3_cor_sd = block3cor_rt['block3cr_rt'].std()
            if len(block3cor_rt["block3cr_rt"]) <= 1:
                b3_cor_sd = 0 
        except:
            b3_cor_sd = 0
            print("Error with 2G GS Block correct sd")

        try:
            b3_com_rt = block3com_rt['block3cm_rt'].mean()
        except:
            b3_com_rt = 0
            print("Error with 2G GS Block commission mean")

        try:
            b3_com_sd = block3com_rt['block3cm_rt'].std()
            if len(block3com_rt["block3cm_rt"]) <= 1:
                b3_com_sd = 0 
        except:
            b3_com_sd = 0
            print("Error with 2G GS Block commission sd")

        try:
            b3_stp_tm = block3cor_stp['block3stp_time_cr'].mean()
        except:
            b3_stp_tm = 0
            print("Error with 2G GS Block correct stop mean")

        try:
            b3_stp_tm_f = block3f_stp['block3stp_time_fail'].mean()
        except:
            b3_stp_tm_f = 0
            print("Error with 2G GS Block failed stop mean")

        #Create Percent correct
        pc_g = (block3_s.target == 'G').sum()
        b3_per_cor_g = b3_cor/pc_g               

        pc_l = (block3_s.target == 'S').sum()
        b3_per_cor_l = b3_rej/pc_l

        #Check to see if participant responded too many times and num of responsses
        b3_sum = (block3_s['block3_resp.keys'] == 'n').sum()
        b3_tot = (block3_s.corrAns3 == 'n').sum() 
        if b3_sum > (b3_tot + b3_comm + 5):
            print("Participant", "has too many responses in 2T GS Block")

        if b3_rej <= 1:
            print("Participant has 1 or less correct rejections in 2T GS Block")
            
        #Create Individual Scored Data
        mask = block3_s.loc[:,'target'] == 'S'
        #ind_scores_2T_gs['2T_gs_cor']= pd.Series([block3_s.loc[mask,['stop_corr']]])
        ind_scores_2T_gs = ind_scores_2T_gs.reset_index(drop=True)

        PGNGS_ind_scores = pd.concat([PGNGS_ind_scores,ind_scores_2T_gs], axis=1)
        
        #Save Scores to scoring dataframe
        PGNGS_scores['2T_gs_hit'] = b3_cor
        PGNGS_scores['2T_gs_omm'] = b3_omm
        PGNGS_scores['2T_gs_comm'] = b3_comm
        PGNGS_scores['2T_gs_reject'] = b3_rej

        PGNGS_scores['2T_gs_rand_com'] = b3_rand_resp

        PGNGS_scores['2T_gs_cor_rt'] = b3_cor_rt
        PGNGS_scores['2T_gs_cor_sd'] = b3_cor_sd

        PGNGS_scores['2T_gs_com_rt'] = b3_com_rt
        PGNGS_scores['2T_gs_com_sd'] = b3_com_sd

        PGNGS_scores['2T_gs_stp_tm'] = b3_stp_tm
        PGNGS_scores['2T_gs_stp_tm_f'] = b3_stp_tm_f

        PGNGS_scores['2T_gs_cor_per_g'] = b3_per_cor_g
        PGNGS_scores['2T_gs_cor_per_l'] = b3_per_cor_l

        PGNGS_clean['target_check'] = block3_s['target']


###########################
#        Save Data        #
###########################
    PGNGS_clean.to_csv((str(out_dir)+'/cleaned/'+str(sub_id) + '_PGNGS_PAVK_cleaned.csv'), index=False)

   # PGNGS_ind_scores.to_csv((str(out_dir)+'/ind_scored/'+str(sub_id) + '_PGNGS_PAVK_ind_scored.csv'), index=False)

    PGNGS_scores.to_csv((str(out_dir)+'/scored/'+str(sub_id) + '_PGNGS_PAVK_scored.csv'), index=False)



