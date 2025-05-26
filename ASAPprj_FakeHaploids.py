#!/usr/bin/env python
# coding: utf-8

# Takes a ped file and insert missing data randomly in the available individuals, but in a progressive fashion so that:
# the first 10 individuals (samples 1st to 10th) will have 10% of missing data, 
# the second 10 (samples from 11th to 20th) 20% of missing data, 
# the third 10 (samples from 21st to 30th) 30% of missing data,
# the fourth 10 (samples from 31st to 40th) 40% of missing data,
# the fifth 10 (samples from 41st to 50th) 50% of missing data
# If the dataset has more than 50 samples, the loop restarts.

# Then, it then creates fake diploid samples, in fact duplicating the number of individuals, and mimicking ancient DNA

# Usage: python script.py input.ped output.ped


import random
# random.seed(123)
from itertools import islice
import csv
import sys

ped_file = sys.argv[1]
aDNA_ped_file = sys.argv[2]


def get_percentage(num_a, num_b):
    return (num_a * num_b) / 100


def createList(n1, n2):
    return [item for item in range(n1, n2)]


def deep_index(lst, w):
    return [(i, sub.index(w)) for (i, sub) in enumerate(lst) if w in sub]


print("Reading your file")

print("Divin' into the loop")
new_index = 0
with open(ped_file) as ped, open(aDNA_ped_file, "w") as output:
    list_row = []
    for index, ind in enumerate(ped):
        PERCENTAGE = 10
        new_index += 1

        if new_index == 51:
            new_index = 1

        elif 0 < new_index < 11:
            PERCENTAGE = 10
        elif 10 < new_index < 21:
            PERCENTAGE = 20
            # print(new_index, PERCENTAGE)
        elif 20 < new_index < 31:
            PERCENTAGE = 30
            # print(new_index, PERCENTAGE)
        elif 30 < new_index < 41:
            PERCENTAGE = 40
            # print(new_index, PERCENTAGE)
        elif 40 < new_index < 51:
            PERCENTAGE = 50
            # print(new_index, PERCENTAGE)

        ind_row = ind.split()  # split() turns content into list, so now every row is turn into a list

        # Creating a list of list with 2 alleles each entry
        coupled_indv_alleles = []
        alleles = iter(ind_row)
        for allele in alleles:
            indv_alleles = [allele, next(alleles)]
            #indv_alleles = []
            #indv_alleles.append(allele)
            #indv_alleles.append(next(alleles))
            coupled_indv_alleles.append(indv_alleles)

        # Now focusing on only the genetic information
        alleles_to_aDNA = coupled_indv_alleles[3:]
        n_alleles_per_indv = len(alleles_to_aDNA)

        # Finding the X% of these alleles and set them to zero
        print("Showing you some numbers, percentages: ", PERCENTAGE)
        n_alleles_to_aDNA = int(get_percentage(n_alleles_per_indv, PERCENTAGE))
        # print(PERCENTAGE)
        target_alleles = random.sample(list(enumerate(alleles_to_aDNA)), n_alleles_to_aDNA)

        indexes = []
        values = []
        for idx, val in target_alleles:
            indexes.append(idx)
            values.append(val)

        # Set indexes as [0,0]
        print("I see dead people now...")
        for x in indexes:
            alleles_to_aDNA[x] = [0, 0]

        # Now we need to resample each item of the [A,T] and create a fake diploid
        # There's something wrong with this loop/order, you should end up with 6 alleles each row

        new_ref_alleles_combinations = []
        new_alt_alleles_combinations = []

        for item in alleles_to_aDNA:
            new_alleles = []
            alt_alleles = []
            random_allele = random.randint(0, 1)

            # ref allele
            new_alleles.append(item[random_allele])
            new_alleles.append(item[random_allele])

            # alt allele
            if random_allele == 0:
                new_random_allele = 1
            else:
                new_random_allele = 0

            alt_alleles.append(item[new_random_allele])
            alt_alleles.append(item[new_random_allele])

            # Write the info in a list of list
            new_ref_alleles_combinations.append(new_alleles)
            new_alt_alleles_combinations.append(alt_alleles)  # <- this needs to go on a separate row

        # all_inds_ped_alleles.append(new_ref_alleles_combinations)
        # all_inds_ped_alleles.append(new_alt_alleles_combinations)

        output.write(' '.join(' '.join(map(str, row)) for row in new_ref_alleles_combinations))
        output.write('\n')
        output.write(' '.join(' '.join(map(str, row)) for row in new_alt_alleles_combinations))
        output.write('\n')
