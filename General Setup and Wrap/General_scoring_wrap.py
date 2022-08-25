##### Wrapper for Pavlovia Scoring


##### In order to run this script, copy and edit sample code below
### description of command: /path/to/this/file/FEPT_PAVK_score_wrap.py -i /path/to/input/csv/file/with/participant/id/labels -d /path/to/folder/where/raw/data/is/stored/ -o /path/to/folder/where/you/want/scored/data/output/to

###you need to have folder with raw data, and excel/csv with column SUBJID followed by subject numbers##

###########################################

import shutil
import time
import os
import sys
import csv
import logging
from argparse import ArgumentParser
import subprocess
from os import listdir
import numpy as np
import pandas as pd

##change to your specific scoring function file and set variable as what you want it to be called
import FEPT_SN_scoring_func as FEPT


logger = logging.getLogger(os.path.basename(__file__))
format="[%(asctime)s][%(levelname)s] - %(name)s - %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG)

def arguments():
    # argument parsing
    parser = ArgumentParser(description="CSV parser and job launcher")
    parser.add_argument("-i", "--input-file", required=True,
        help="Input CSV file")
    parser.add_argument("-o", "--output-base", required=True,
        help="Base Output Directory")
    parser.add_argument("-d", "--data-loc", required=True,
        help="Data Location")
    return parser

def main():
    parser = arguments()
    args = parser.parse_args()

    # expand any ~/ in filenames
    args.input_file = os.path.expanduser(args.input_file)
    args.output_base = os.path.expanduser(args.output_base)
    args.data_loc = os.path.expanduser(args.data_loc)

    #Create Input and Output
    # create base and output directory variable
    
    outdir = os.path.join(args.output_base)
    logger.info("outdir: %s" % outdir)

    datadir = os.path.join(args.data_loc)
    logger.info("datadir: %s" % datadir)

    #Create directories
    directory_c = "cleaned"
    directory_s = "scored"
    directory_is = 'ind_scored'
      
    path_c = os.path.join(outdir, directory_c)
    path_s = os.path.join(outdir, directory_s)
    path_is = os.path.join(outdir, directory_is)
    
    if os.path.isdir(path_c) == False:
        os.mkdir(path_c)
        logger.info("Directory '% s' created" % directory_c)
    else:
        logger.info("Directory '% s' already exists -- continuing" % directory_c)

    if os.path.isdir(path_s) == False:
        os.mkdir(path_s)
        logger.info("Directory '% s' created" % directory_s)
    else:
        logger.info("Directory '% s' already exists -- continuing" % directory_s)

    if os.path.isdir(path_is) == False:
        os.mkdir(path_is)
        logger.info("Directory '% s' created" % directory_is)
    else:
        logger.info("Directory '% s' already exists -- continuing" % directory_is)


    # check for the csv file
    if not os.path.exists(args.input_file):
        logger.error("path does not exist %s" % args.input_file)
        sys.exit(1)
    
    # iterate over csv file
    with open(args.input_file, "r") as fd:
        reader = csv.reader(fd)
        headers = next(reader)
        for i,row in enumerate(reader, 1):
            # zip headers with row data
            row = dict(zip(headers, row))
            # validate the contents of the current row
            if not row["SUBJID"]:
                logger.fatal("csv row %s has empty session" % i)
                continue
            subj_id = row["SUBJID"]

            logger.info("subj_id=%s" % (subj_id))


            # Pause the script for 10 seconds
            time.sleep(10)            

            #More arguments 
            def arguments2():
                 # argument parsing
                parser = ArgumentParser(description="CSV parser and job launcher")
                parser.add_argument("-s", "--subj-id", required=True,
                        help="Subject ID")
                parser.add_argument("-n", "--subj-num", required=True,
                        help="Subjects number in list")
                return parser

            def main2():
                parser = arguments2()
                args = parser.parse_args()            

            #cmd = running the main script  -- change to specific scoring function name
            cmd = "FEPT.FEPT_SN_scoring_func(%s %s %s)" % (subj_id, outdir, datadir)
            # change to scoring function name
            FEPT.FEPT_SN_scoring_func(subj_id, outdir, datadir)
            
	    # sbatch the command
            logger.info("executing command: %s" % cmd)

            
if __name__ == "__main__":
        main()

