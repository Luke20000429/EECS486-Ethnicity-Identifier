import os
import sys

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
