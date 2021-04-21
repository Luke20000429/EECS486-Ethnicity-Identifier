import os
import sys

def readData(regionINFO='data/regions.txt', nameINFO='data/redb.txt'):

    # read in data
    
    regions = []
    name_pairs = []

    with open(regionINFO, 'r', encoding='utf-8') as f:
        for line in f:
            region = line[:-1].split(" ")[0]
            regions.append(region) ## #line:region_id num_of_data
            

    with open(nameINFO, 'r', encoding='utf-8') as f:
        for line in f:
            na_re = line[:-1].split(" ")
            na_re[1] = int(na_re[1])
            name_pairs.append(tuple(na_re)) ## name region_id

    return regions, name_pairs

