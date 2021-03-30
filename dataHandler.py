import os
import sys

def readData(regionINFO='data/regions.txt', nameINFO='data/redb.txt'):
    
    regions = []
    name_pairs = []

    with open(regionINFO, 'r', encoding='utf-8') as f:
        for line in f:
            region = line[:-1]
            regions.append(region) ## #line:region_id region
            

    with open(nameINFO, 'r', encoding='utf-8') as f:
        for line in f:
            na_na = line[:-1].split(" ")
            na_na[1] = int(na_na[1])
            name_pairs.append(tuple(na_na)) ## name region_id

    return regions, name_pairs

