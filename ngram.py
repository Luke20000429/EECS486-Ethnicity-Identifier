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

def getFix(N, pairs, regions, order=1):
    ## get pre/suffix for different regions
    ## sorted by popularity
    ## order=1 prefix, order=-1 suffix
    print("get pre/suffix")
    print("To use: prefix[ethnicity_id]")
    if order==1:
        prefix = [dict() for i in regions]
        for name, rid in pairs:
            _fix = name[0:N]
            if _fix in prefix[rid].keys():
                prefix[rid][_fix] += 1
            else:
                prefix[rid][_fix] = 1
        sorted_prefix = []
        for rid in range(len(regions)): 
            sorted_prefix.append(sorted(prefix[rid].items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
        return sorted_prefix

    elif order==-1:
        suffix = [dict() for i in regions]
        for name, rid in pairs:
            _fix = name[-N:]
            if _fix in suffix[rid].keys():
                suffix[rid][_fix] += 1
            else:
                suffix[rid][_fix] = 1
        sorted_suffix = []
        for rid in range(len(regions)): 
            sorted_suffix.append(sorted(suffix[rid].items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
        return sorted_suffix

def getGrams(name):
    ## split a name into uni/bi/tri-grams
    grams = []
    for N in range(3):
        grams.append([])
        for i in range(N, len(name)):
            grams[N].append(name[i-N:i+1])

    return grams


if __name__ == '__main__':
    print("get grams demo")
    print(getGrams("liuxueshen"))
    
