import os
import sys
import codecs
import math
import numpy as np

def readData(regionINFO='regions.txt', nameINFO='redb.txt'):
    
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

def getNgrams(N, pairs, regions):
    ngrams = [dict() for i in regions]
    N = N-1
    for name, rid in pairs:
        for i in range(N, len(name)):
            gram = name[i-N:i+1]
            if gram in ngrams[rid].keys():
                ngrams[rid][gram] += 1
            else:
                ngrams[rid][gram] = 1

    return ngrams
