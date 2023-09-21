#!/usr/bin/env python
# coding: utf-8

# Goal: find the two PCs that maximise d per each POP

import pandas as pd
from itertools import combinations
import math

PCA_FILE = 'PRJ-0.100.pca.evec'
SOURCES = ["AFR4", "EUR1", "EUR2", "EUR3", "ASN1", "ASN2", "ASN3"]
PC_COUNT = 100

pcx = ["POP", "ID"]
for i in range(1, PC_COUNT+1):
    pc_tmp = "PC" + str(i)
    pcx.append(pc_tmp)

pcx.append('CC')

# The dataset is subsetted to focus on the SOURCES only

df = pd.read_csv(PCA_FILE, skiprows=1, sep='\s+|\t| ', header=None, names=pcx, engine='python')
df_sources = df[df['POP'].isin(SOURCES)]

# Get mean or median values within each group/source

mean_values = df_sources.groupby(by="POP").mean()
median_values = df_sources.groupby(by="POP").median()

# EUCLIDEAN DISTANCE

# d = sqrt[(x2-x1)^2+(y2-y1)^2]

colnames = list(df.columns)[2:-1]
# comb_of_colnames = sorted(map(sorted, combinations(set(colnames),2)))
# comb_of_sources = sorted(map(sorted, combinations(set(SOURCES),2)))

comb_of_colnames = [['PC1', 'PC2'], ['PC2', 'PC3']]
comb_of_sources = [['AFR4', 'EUR1'], ['EUR1', 'EUR2']]

eucl_dist_df = []
# Loop through PCs
for comb in comb_of_colnames:
    tmp = median_values[comb]
    names = list(tmp.columns)
    tmp = tmp.reset_index()

    # Loop through Sources
    for comb_sources in comb_of_sources:
        print('Analysing:', comb_sources, "for", comb)
        target_pair = tmp[tmp['POP'].isin(comb_sources)]

        # Euclidean distance estimation
        x1 = float(target_pair.iloc[0, 1])
        x2 = float(target_pair.iloc[0, 2])
        y1 = float(target_pair.iloc[1, 1])
        y2 = float(target_pair.iloc[1, 2])
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        print('Distance is: ', d)

        # Save estimation in a decent manner
        column_name = '-'.join(comb)
        index_name = '-'.join(comb_sources)
        tmp_df = pd.DataFrame({'PopPairs': index_name, column_name: [d], })
        eucl_dist_df.append(tmp_df)

eucl_dist_df = pd.concat(eucl_dist_df, axis=0)
Distances = pd.concat([df1.apply(lambda x: sorted(x, key=pd.isnull)) for _, df1 in eucl_dist_df.groupby('PopPairs')]).dropna()

Distances.to_csv('euclidean_dist_megamatrix.csv')
