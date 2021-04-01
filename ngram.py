import os
import sys

def getNgrams(N, pairs, regions):
    ## get data of uni/bi/tri-grams
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

def getGrams(name):
    ## split a name into uni/bi/tri-grams
    grams = []
    for N in range(3):
        grams.append([])
        for i in range(N, len(name)):
            grams[N].append(name[i-N:i+1])

    return grams


if __name__ == '__main__':
    print(getGrams("liuxueshen"))
    
