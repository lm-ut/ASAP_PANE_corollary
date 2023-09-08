#!/usr/bin/env python
# coding: utf-8

# Running BlockJackknife
# In order to get mean and sd dev for each PC
#
# To do so, we need to:
# Take bim file, get TOT positions and divide by N
# N = len(Bim)/N
#
# N will be the number of positions that we need to remove each time we ran the PCA.
# Specifically, we need to remove the FIRST N, the SECOND N, the THIRD N and so on
#
# ie, bim file is 100:
#
# N = 100/20 = 5
#
# pos 0-4 removed -> convert to eigen -> pca \
# pos 5-9 removed -> convert to eigen -> pca \
# pos 10-14 removed -> convert to eigen -> pca \
#
# etc
#
# The N PCAs obtained can then be set as input in ASAP R package, please refer to ASAP manual

import pandas as pd
import subprocess
import os
import glob
import numbers
import sys

file_name = sys.argv[1]

# Estimating length of bim
num_lines = sum(1 for line in open(file_name + '.bim'))

# Num of blocks (or PCA that will be ran)
nblocks = 20

# Estimating block size (or the N of SNPs to remove each iteration)
block_length = round(num_lines / nblocks)

run = 1

for block in range(0, num_lines, block_length):
    block_start = block
    block_end = block + block_length
    print("In this round, I am removing pos " + str(block_start), "to", str(block_end))
    plink = pd.read_csv(file_name + ".bim", sep='\t', header=None)

    POS = plink.iloc[block_start:block_end]
    ID_POS = POS.iloc[:, 1]
    ID_POS.to_csv('POS_run' + str(run), header=None, index=None)

    bashCommand = ['plink --bfile ' + file_name + " --exclude POS_run" + str(run) + " --make - bed - -out "+file_name+"_Jackknife_"+str(run)]
    process_plink = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
    output, error = process_plink.communicate()

    run += 1

    for run in range(1, 21):
        jack_file_name = file_name + "_Jackknife_" + str(run)

        # Create par file
        BED2EIG_Command = ["bash BED2EIG.sh " + jack_file_name + " " + jack_file_name]
        process_bed2eig = subprocess.Popen(BED2EIG_Command, stdout=subprocess.PIPE, shell=True)
        output, error = process_bed2eig.communicate()

        CC_Command = ["echo Control > pop_list.txt"]
        process_cc = subprocess.Popen(CC_Command, stdout=subprocess.PIPE, shell=True)
        output, error = process_cc.communicate()
