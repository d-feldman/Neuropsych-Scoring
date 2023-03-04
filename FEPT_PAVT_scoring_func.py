#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#######################################################################################
#######################################################################################
# PGNGS Scoring Script/Function for Pavlovia Keyboard Data                               
# Last edited 20221012
#######################################################################################
#######################################################################################

def FEPT_PAVT_scoring_func(sub_id, out_dir, data_dir):

#######################################################################################
#Please Make edits to the specifications listed below as indicated by the instructions
#If unsure how to proceed, please contact the MEND2 Lab
#######################################################################################
    ## These parameters are based on how you set up your PGNGS experience. If unsure, most of these
    ## can be found by looking at some of your output data.


############# Options
    ##Key Options
    #Happy
    h_key = 'buttonHappy'

    #Sad
    s_key = 'buttonSad'

    #Fear
    f_key = 'buttonFear'

    #Ang
    a_key = 'buttonAngry'

    #Neutral
    n_key = 'buttonNeut'

    ##Timing
    face_time = .5
    anim_time = .5
    mask_time = .125

############################################################################################
############################################################################################
                    #DO NOT MAKE ANY CHANGES BEYOND THIS POINT
############################################################################################
############################################################################################

    #############################
    #          SETUP            #
    #############################

    import numpy as np
    import pandas as pd
    from functools import reduce
    import csv
    import re
    import sys

    part_id = sub_id

    FEPT_data = pd.read_csv((str(data_dir) + '/' + str(sub_id) + 'FEPT_PAVT.CSV'), header=0, sep=",")


    FEPT_scores = pd.DataFrame(np.zeros((1,1)), columns=['user_id'])

    FEPT_scores['user_id'] = part_id

    ###########################
    #      Faces Scoring      #
    ###########################

    # Create main faces dataframe
    faces_set = FEPT_data[["Stimuli", "corr.Ans", "mouseFaces.clicked_name", "mouseFaces.time", "mouseFaces.leftButton"]]

    faces_clean = faces_set[faces_set['Stimuli'].notna()]
    faces_clean = faces_clean.reset_index(drop=True)

    ## Set up Blank Variables
    hap_corr_rt = pd.DataFrame()
    hap_incorr_rt = pd.DataFrame()

    sad_corr_rt = pd.DataFrame()
    sad_incorr_rt = pd.DataFrame()

    fear_corr_rt = pd.DataFrame()
    fear_incorr_rt = pd.DataFrame()

    ang_corr_rt = pd.DataFrame()
    ang_incorr_rt = pd.DataFrame()

    neut_corr_rt = pd.DataFrame()
    neut_incorr_rt = pd.DataFrame()

    hap_corr = 0
    hap_as_sad = 0
    hap_as_fear = 0
    hap_as_ang = 0
    hap_as_neut = 0
    hap_as_none = 0

    sad_corr = 0
    sad_as_hap = 0
    sad_as_fear = 0
    sad_as_ang = 0
    sad_as_neut = 0
    sad_as_none = 0

    fear_corr = 0
    fear_as_hap = 0
    fear_as_sad = 0
    fear_as_ang = 0
    fear_as_neut = 0
    fear_as_none = 0

    ang_corr = 0
    ang_as_hap = 0
    ang_as_sad = 0
    ang_as_fear = 0
    ang_as_neut = 0
    ang_as_none = 0

    neut_corr = 0
    neut_as_hap = 0
    neut_as_sad = 0
    neut_as_fear = 0
    neut_as_ang = 0
    neut_as_none = 0


    ## Main Faces Scores
    for i in range(len(faces_clean)):

        #for key in key_list: I think you might be able to make this even more applicable to other versions by
        #using another for loop (idea above) and iterating through each key, not sure though, might be too complicated
        if faces_clean.loc[i, "corr.Ans"] == h_key:
            if faces_clean.loc[i, "mouseFaces.clicked_name"] == h_key:
                hap_corr = hap_corr + 1
                hap_corr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == s_key:
                hap_as_sad = hap_as_sad + 1
                hap_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == f_key:
                hap_as_fear = hap_as_fear + 1
                hap_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == a_key:
                hap_as_ang = hap_as_ang + 1
                hap_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == n_key:
                hap_as_neut = hap_as_neut + 1
                hap_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] is np.nan:
                hap_as_none = hap_as_none + 1
            else:
                continue

        elif faces_clean.loc[i, "corr.Ans"] == s_key:
            if faces_clean.loc[i, "mouseFaces.clicked_name"] == s_key:
                sad_corr = sad_corr + 1
                sad_corr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == h_key:
                sad_as_hap = sad_as_hap + 1 
                sad_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == f_key:
                sad_as_fear = sad_as_fear + 1
                sad_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == a_key:
                sad_as_ang = sad_as_ang + 1
                sad_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == n_key:
                sad_as_neut = sad_as_neut + 1
                sad_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] is np.nan:
                sad_as_none = sad_as_none + 1
            else:
                continue

        elif faces_clean.loc[i, "corr.Ans"] == f_key:
            if faces_clean.loc[i, "mouseFaces.clicked_name"] == f_key:
                fear_corr = fear_corr + 1
                fear_corr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == h_key:
                fear_as_hap = fear_as_hap + 1 
                fear_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == s_key:
                fear_as_sad = fear_as_sad + 1 
                fear_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == a_key:
                fear_as_ang = fear_as_ang + 1 
                fear_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == n_key:
                fear_as_neut = fear_as_neut + 1 
                fear_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == 'None':
                fear_as_none = fear_as_none + 1 
            else:
                continue

        elif faces_clean.loc[i, "corr.Ans"] == a_key:
            if faces_clean.loc[i, "mouseFaces.clicked_name"] == a_key:
                ang_corr = ang_corr + 1
                ang_corr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == h_key:
                ang_as_hap = ang_as_hap + 1 
                ang_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == s_key:
                ang_as_sad = ang_as_sad + 1
                ang_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == f_key:
                ang_as_fear = ang_as_fear + 1
                ang_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == n_key:
                ang_as_neut = ang_as_neut + 1
                ang_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] is np.nan:
                ang_as_none = ang_as_none + 1
            else:
                continue

        elif faces_clean.loc[i, "corr.Ans"] == n_key:
            if faces_clean.loc[i, "mouseFaces.clicked_name"] == n_key:
                neut_corr = neut_corr + 1
                neut_corr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == h_key:
                neut_as_hap = neut_as_hap + 1
                neut_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == s_key:
                neut_as_sad = neut_as_sad + 1
                neut_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == f_key:
                neut_as_fear = neut_as_fear + 1
                neut_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] == a_key:
                neut_as_ang = neut_as_ang + 1
                neut_incorr_rt.loc[i, "rt"] = face_time + mask_time + faces_clean.loc[i,"mouseFaces.time"]
            elif faces_clean.loc[i, "mouseFaces.clicked_name"] is np.nan:
                neut_as_none = neut_as_none + 1
            else:
                continue
        else:
            continue



    ##Response times
    #Happy 
    hap_corr_rt = hap_corr_rt.reset_index(drop=True)
    try:
        hap_cor_rt = hap_corr_rt["rt"].mean()
    except:
        try:
            if len(hap_corr_rt["rt"]) == 1:
                hap_cor_rt = hap_corr_rt.loc[i, "rt"]
        except:
            hap_cor_rt = -999
            print("Error with Happy correct RT Mean")
    try:
        hap_cor_sd = hap_corr_rt["rt"].std()
        if len(hap_corr_rt["rt"]) <= 1:
            hap_cor_sd = -999 
    except:
        hap_cor_sd = -999
        print("Error with Happy Correct RT SD")

    hap_incorr_rt = hap_incorr_rt.reset_index(drop=True)    
    try:
        hap_incor_rt = hap_incorr_rt["rt"].mean()
    except:
        try:
            if len(hap_incorr_rt["rt"]) == 1:
                hap_incor_rt = hap_incorr_rt.loc[i, "rt"]
        except:
            hap_incor_rt = -999
            print("Error with Happy Incorrect RT Mean")
    try:
        hap_incor_sd = hap_incorr_rt["rt"].std()
        if len(hap_incorr_rt["rt"]) <= 1:
            hap_incor_sd = -999 
    except:
        hap_incor_sd = -999
        print("Error with Happy Incorrect RT SD")

    #Sad 
    sad_corr_rt = sad_corr_rt.reset_index(drop=True)
    try:
        sad_cor_rt = sad_corr_rt["rt"].mean()
    except:
        try:
            if len(sad_corr_rt["rt"]) == 1:
                sad_cor_rt = sad_corr_rt.loc[i, "rt"]
        except:
            sad_cor_rt = -999
            print("Error with Sad correct RT Mean")

    try:
        sad_cor_sd = sad_corr_rt["rt"].std()
        if len(sad_corr_rt["rt"]) <= 1:
            sad_cor_sd = -999 
    except:
        sad_cor_sd = -999
        print("Error with Sad Correct RT SD")

    sad_incorr_rt = sad_incorr_rt.reset_index(drop=True)
    try:
        sad_incor_rt = sad_incorr_rt["rt"].mean()
    except:
        try:
            if len(sad_incorr_rt["rt"]) == 1:
                sad_incor_rt = sad_incorr_rt.loc[i, "rt"]
        except:
            sad_incor_rt = -999
            print("Error with Sad Incorrect RT Mean")

    try:
        sad_incor_sd = sad_incorr_rt["rt"].std()
        if len(sad_incorr_rt["rt"]) <= 1:
            sad_incor_sd = -999 
    except:
        sad_incor_sd = -999
        print("Error with Sad Incorrect RT SD")

    #Fear 
    fear_corr_rt = fear_corr_rt.reset_index(drop=True)
    try:
        fear_cor_rt = fear_corr_rt["rt"].mean()
    except:
        try:
            if len(fear_corr_rt["rt"]) == 1:
                fear_cor_rt = fear_corr_rt.loc[i, "rt"]
        except:
            fear_cor_rt = -999
            print("Error with Fear correct RT Mean")

    try:
        fear_cor_sd = fear_corr_rt["rt"].std()
        if len(fear_corr_rt["rt"]) <= 1:
            fear_cor_sd = -999 
    except:
        fear_cor_sd = -999
        print("Error with Fear Correct RT SD")

    fear_incorr_rt = fear_incorr_rt.reset_index(drop=True)
    try:
        fear_incor_rt = fear_incorr_rt["rt"].mean()
    except:
        try:
            if len(fear_incorr_rt["rt"]) == 1:
                fear_incor_rt = fear_incorr_rt.loc[i, "rt"]
        except:
            fear_incor_rt = -999
            print("Error with Fear Incorrect RT Mean")

    try:
        fear_incor_sd = fear_incorr_rt["rt"].std()
        if len(fear_incorr_rt["rt"]) <= 1:
            fear_incor_sd = -999
    except:
        fear_incor_sd = -999
        print("Error with Fear Incorrect RT SD")

    #Anger
    ang_corr_rt = ang_corr_rt.reset_index(drop=True)
    try:
        ang_cor_rt = ang_corr_rt["rt"].mean()
    except:
        try:
            if len(ang_corr_rt["rt"]) == 1:
                ang_cor_rt = ang_corr_rt.loc[i, "rt"]
        except:
            ang_cor_rt = -999
            print("Error with Anger correct RT Mean")

    try:
        ang_cor_sd = ang_corr_rt["rt"].std()
        if len(ang_corr_rt["rt"]) <= 1:
            ang_cor_sd = -999
    except:
        ang_cor_sd = -999
        print("Error with Anger Correct RT SD")

    ang_incorr_rt = ang_incorr_rt.reset_index(drop=True)
    try:
        ang_incor_rt = ang_incorr_rt["rt"].mean()
    except:
        try:
            if len(ang_incorr_rt["rt"]) == 1:
                ang_incor_rt = ang_incorr_rt.loc[i, "rt"]
        except:
            ang_incor_rt = -999
            print("Error with Anger Incorrect RT Mean")

    try:
        ang_incor_sd = ang_incorr_rt["rt"].std()
        if len(ang_incorr_rt["rt"]) <= 1:
            ang_incor_sd = -999 
    except:
        ang_incor_sd = -999
        print("Error with Anger Incorrect RT SD")

    #Neutral
    neut_corr_rt = neut_corr_rt.reset_index(drop=True)
    try:
        neut_cor_rt = neut_corr_rt["rt"].mean()
    except:
        try:
            if len(neut_corr_rt["rt"]) == 1:
                neut_cor_rt = neut_corr_rt.loc[i, "rt"]
        except:
            neut_cor_rt = -999
            print("Error with Neutral correct RT Mean")

    try:
        neut_cor_sd = neut_corr_rt["rt"].std()
        if len(neut_corr_rt["rt"]) <= 1:
            neut_cor_sd = -999
    except:
        neut_cor_sd = -999
        print("Error with Neutral Correct RT SD")

    neut_incorr_rt = neut_incorr_rt.reset_index(drop=True)
    try:
        neut_incor_rt = neut_incorr_rt["rt"].mean()
    except:
        try:
            if len(neut_incorr_rt["rt"]) == 1:
                neut_incor_rt = neut_incorr_rt.loc[, "rt"]
        except:
            neut_incor_rt = -999
            print("Error with Neutral Incorrect RT Mean")
    try:
        neut_incor_sd = neut_incorr_rt["rt"].std()
        if len(neut_incorr_rt["rt"]) <= 1:
            neut_incor_sd = -999
    except:
        neut_incor_sd = -999
        print("Error with Neutral Incorrect RT SD")


    #All
    #Create total correct rt dataframe
    face_cor_rt_comb_data = pd.DataFrame()

    try:
        face_cor_rt_comb_data = face_cor_rt_comb_data.append(hap_corr_rt)
    except:
        pass
    try: 
        face_cor_rt_comb_data = face_cor_rt_comb_data.append(sad_corr_rt)
    except:
        pass
    try: 
        face_cor_rt_comb_data = face_cor_rt_comb_data.append(fear_corr_rt)
    except:
        pass
    try: 
        face_cor_rt_comb_data = face_cor_rt_comb_data.append(ang_corr_rt)
    except:
        pass
    try: 
        face_cor_rt_comb_data = face_cor_rt_comb_data.append(neut_corr_rt)
    except:
        pass
    try:
        face_cor_rt_comb_data = face_cor_rt_comb_data.reset_index(drop=True)
    except:
        pass

    #Create total incorrect rt dataframe
    face_incor_rt_comb_data = pd.DataFrame()

    try:
        face_incor_rt_comb_data = face_incor_rt_comb_data.append(hap_incorr_rt)
    except:
        pass
    try: 
        face_incor_rt_comb_data = face_incor_rt_comb_data.append(sad_incorr_rt)
    except:
        pass
    try: 
        face_incor_rt_comb_data = face_incor_rt_comb_data.append(fear_incorr_rt)
    except:
        pass
    try: 
        face_incor_rt_comb_data = face_incor_rt_comb_data.append(ang_incorr_rt)
    except:
        pass
    try: 
        face_incor_rt_comb_data = face_incor_rt_comb_data.append(neut_incorr_rt)
    except:
        pass
    try:
        face_incor_rt_comb_data = face_incor_rt_comb_data.reset_index(drop=True)
    except:
        pass

    allFaces_rt_comb_data = face_cor_rt_comb_data.append(face_incor_rt_comb_data)
    allFaces_rt_comb_data = allFaces_rt_comb_data.reset_index(drop=True)

    # Response time Means/SD
    face_cor_rt_comb_data = face_cor_rt_comb_data.reset_index(drop=True)
    try:
        faces_cor_rt = face_cor_rt_comb_data["rt"].mean()
    except:
        try:
            if len(face_cor_rt_comb_data["rt"]) == 1:
                faces_cor_rt = face_cor_rt_comb_data.loc[i, "rt"]
        except:
            faces_cor_rt = -999
            print("Error with All Faces Correct RT Mean")
    try:
        faces_cor_sd = face_cor_rt_comb_data["rt"].std()
        if len(face_cor_rt_comb_data["rt"]) <= 1:
            faces_cor_sd = -999 
    except:
        faces_cor_sd = -999
        print("Error with All Faces Correct RT SD")

    face_incor_rt_comb_data = face_incor_rt_comb_data.reset_index(drop=True)
    try:
        faces_incor_rt = face_incor_rt_comb_data["rt"].mean()
    except:
        try:
            if len(face_incor_rt_comb_data["rt"]) == 1:
                faces_incor_rt = face_incor_rt_comb_data.loc[i, "rt"]
        except:
            faces_incor_rt = -999
            print("Error with All Faces Incorrect RT Mean")

    try:
        faces_incor_sd = face_incor_rt_comb_data["rt"].std()
        if len(face_incor_rt_comb_data["rt"]) <= 1:
            faces_incor_sd = -999 
    except:
        faces_incor_sd = -999
        print("Error with All Faces Incorrect RT SD")

    allFaces_rt_comb_data = allFaces_rt_comb_data.reset_index(drop=True)
    try:
        allFaces_rt = allFaces_rt_comb_data["rt"].mean()
    except:
        try:
            if len(allFaces_rt_comb_data["rt"]) == 1:
                allFaces_rt = allFaces_rt_comb_data.loc[i, "rt"]
        except:
            allFaces_rt = -999
            print("Error with All Faces RT Mean")
    try:
        allFaces_sd = allFaces_rt_comb_data["rt"].std()
        if len(allFaces_rt_comb_data["rt"]) <= 1:
            allFaces_sd = -999 
    except:
        allFaces_sd = -999
        print("Error with All Faces RT SD")

    ##Other Scores
    #False Alarms
    hap_false_alarm = sad_as_hap + fear_as_hap + ang_as_hap + neut_as_hap

    sad_false_alarm = hap_as_sad + fear_as_sad + ang_as_sad + neut_as_sad

    fear_false_alarm = hap_as_fear + sad_as_fear + ang_as_fear + neut_as_fear

    ang_false_alarm = hap_as_ang + sad_as_ang + fear_as_ang + neut_as_ang

    neut_false_alarm = hap_as_neut + sad_as_neut + fear_as_neut + ang_as_neut

    none_all = hap_as_none + sad_as_none + fear_as_none + ang_as_none + neut_as_none


    #General
    faces_corr = hap_corr + sad_corr + fear_corr + ang_corr + neut_corr
    faces_incor = hap_false_alarm + sad_false_alarm + fear_false_alarm + ang_false_alarm + neut_false_alarm + none_all

    ### Save all scores 
    FEPT_scores['faces_corr'] = faces_corr
    FEPT_scores['faces_incor'] = faces_incor

    FEPT_scores['allFaces_rt'] = allFaces_rt
    FEPT_scores['allFaces_sd'] = allFaces_sd

    FEPT_scores['faces_cor_rt'] = faces_cor_rt
    FEPT_scores['faces_cor_sd'] = faces_cor_sd
    FEPT_scores['faces_incor_rt'] = faces_incor_rt
    FEPT_scores['faces_incor_sd'] = faces_incor_sd

    FEPT_scores['hap_corr'] = hap_corr
    FEPT_scores['hap_as_sad'] = hap_as_sad
    FEPT_scores['hap_as_fear'] = hap_as_fear
    FEPT_scores['hap_as_ang'] = hap_as_ang
    FEPT_scores['hap_as_neut'] = hap_as_neut
    FEPT_scores['hap_as_none'] = hap_as_none

    FEPT_scores['hap_false_alarm'] = hap_false_alarm

    FEPT_scores['hap_cor_rt'] = hap_cor_rt
    FEPT_scores['hap_cor_sd'] = hap_cor_sd
    FEPT_scores['hap_incor_rt'] = hap_incor_rt
    FEPT_scores['hap_incor_sd'] = hap_incor_sd

    FEPT_scores['sad_corr'] = sad_corr
    FEPT_scores['sad_as_hap'] = sad_as_hap
    FEPT_scores['sad_as_fear'] = sad_as_fear
    FEPT_scores['sad_as_ang'] = sad_as_ang
    FEPT_scores['sad_as_neut'] = sad_as_neut
    FEPT_scores['sad_as_none'] = sad_as_none

    FEPT_scores['sad_false_alarm'] = sad_false_alarm

    FEPT_scores['sad_cor_rt'] = sad_cor_rt
    FEPT_scores['sad_cor_sd'] = sad_cor_sd
    FEPT_scores['sad_incor_rt'] = sad_incor_rt
    FEPT_scores['sad_incor_sd'] = sad_incor_sd

    FEPT_scores['fear_corr'] = fear_corr
    FEPT_scores['fear_as_hap'] = fear_as_hap
    FEPT_scores['fear_as_sad'] = fear_as_sad
    FEPT_scores['fear_as_ang'] = fear_as_ang
    FEPT_scores['fear_as_neut'] = fear_as_neut
    FEPT_scores['fear_as_none'] = fear_as_none

    FEPT_scores['fear_false_alarm'] = fear_false_alarm

    FEPT_scores['fear_cor_rt'] = fear_cor_rt
    FEPT_scores['fear_cor_sd'] = fear_cor_sd
    FEPT_scores['fear_incor_rt'] = fear_incor_rt
    FEPT_scores['fear_incor_sd'] = fear_incor_sd

    FEPT_scores['ang_corr'] = ang_corr
    FEPT_scores['ang_as_hap'] = ang_as_hap
    FEPT_scores['ang_as_sad'] = ang_as_sad
    FEPT_scores['ang_as_fear'] = ang_as_fear
    FEPT_scores['ang_as_neut'] = ang_as_neut
    FEPT_scores['ang_as_none'] = ang_as_none

    FEPT_scores['ang_false_alarm'] = ang_false_alarm

    FEPT_scores['ang_cor_rt'] = ang_cor_rt
    FEPT_scores['ang_cor_sd'] = ang_cor_sd
    FEPT_scores['ang_incor_rt'] = ang_incor_rt
    FEPT_scores['ang_incor_sd'] = ang_incor_sd

    FEPT_scores['neut_corr'] = neut_corr
    FEPT_scores['neut_as_hap'] = neut_as_hap
    FEPT_scores['neut_as_sad'] = neut_as_sad
    FEPT_scores['neut_as_fear'] = neut_as_fear
    FEPT_scores['neut_as_ang'] = neut_as_ang
    FEPT_scores['neut_as_none'] = neut_as_none

    FEPT_scores['neut_false_alarm'] = neut_false_alarm

    FEPT_scores['neut_cor_rt'] = neut_cor_rt
    FEPT_scores['neut_cor_sd'] = neut_cor_sd
    FEPT_scores['neut_incor_rt'] = neut_incor_rt
    FEPT_scores['neut_incor_sd'] = neut_incor_sd

    FEPT_scores['none_sum'] = none_all



    ###########################
    #     Animal Scoring      #
    ###########################

    animals_set = FEPT_data[["Stimulus", "corr.Ans", "mouseAnimals.clicked_name", "mouseAnimals.time", "mouseAnimals.leftButton"]]


    animals_clean = animals_set[animals_set['Stimulus'].notna()]
    animals_clean = animals_clean.reset_index(drop=True)

    #Set up blank scores
    anim_corr = 0
    anim_incor = 0
    anim_corr_rt = pd.DataFrame()
    anim_incorr_rt = pd.DataFrame()

    ## Main Scores
    for i in range(len(animals_clean)):
        if animals_clean.loc[i, "corr.Ans"] == animals_clean.loc[i, "mouseAnimals.clicked_name"]:
            anim_corr = anim_corr + 1
            anim_corr_rt.loc[i, "rt"] = anim_time + mask_time + animals_clean.loc[i,"mouseAnimals.time"]
        else:
            anim_incor = anim_incor + 1
            anim_incorr_rt.loc[i, "rt"] = anim_time + mask_time + animals_clean.loc[i,"mouseAnimals.time"]


    ### Other Scores
    ##Response Times
    anim_corr_rt = anim_corr_rt.reset_index(drop=True)
    try:
        anim_cor_rt = anim_corr_rt["rt"].mean()
    except:
        try:
            if len(anim_corr_rt["rt"]) == 1:
                anim_cor_rt = anim_corr_rt.loc[i, "rt"]
        except:
            anim_cor_rt = -999
            print("Error with Animal Correct RT Mean")
    try:
        anim_cor_sd = anim_corr_rt["rt"].std()
        if len(anim_corr_rt["rt"]) <= 1:
            anim_cor_sd = -999
    except:
        anim_cor_sd = -999
        print("Error with Animals Correct RT SD")

    anim_incorr_rt = anim_incorr_rt.reset_index(drop=True)
    try:
        anim_incor_rt = anim_incorr_rt["rt"].mean()
    except:
        try:
            if len(anim_incorr_rt["rt"]) == 1:
                anim_incor_rt = anim_incorr_rt.loc[i, "rt"]
        except:
            anim_incor_rt = -999
            print("Error with Animal Incorrect RT Mean")

    try:
        anim_incor_sd = anim_incorr_rt["rt"].std()
        if len(anim_incorr_rt["rt"]) <= 1:
            anim_incor_sd = -999 
    except:
        anim_incor_sd = -999
        print("Error with Animals Incorrect RT SD")

    #Save all animal scores
    FEPT_scores['anim_corr'] = anim_corr
    FEPT_scores['anim_incor'] = anim_incor

    FEPT_scores['anim_cor_rt'] = anim_cor_rt
    FEPT_scores['anim_cor_sd'] = anim_cor_sd
    FEPT_scores['anim_incor_rt'] = anim_incor_rt
    FEPT_scores['anim_incor_sd'] = anim_incor_sd


    faces_clean = faces_clean.rename(columns={"mouseFaces.clicked_name": "part_response", "corr.Ans": "correct", "mouseFaces.time": "response_time"})
    animals_clean = animals_clean.rename(columns={ "Stimulus":"Stimuli", "mouseAnimals.clicked_name": "part_response", "corr.Ans": "correct", "mouseAnimals.time": "response_time"})

    FEPT_clean = faces_clean.append(animals_clean)

    ###########################
    #        Save Data        #
    ###########################
    FEPT_clean.to_csv((str(out_dir)+'/'+str(sub_id) + 'FEPT_PAVT_cleaned.csv'), index=False)


    FEPT_scores.to_csv((str(out_dir)+'/'+str(sub_id) + 'FEPT_PAVT_scored.csv'), index=False)
    

