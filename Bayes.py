import os
import sys
import codecs
import math
import numpy as np
from dataHandler import readData
from ngram import getNgrams, getGrams

def getPc():
    ## get possibility of each cate
    regions, name_pairs = readData()
    Pc = []
    for re, num in regions:
        Pc.append(math.log(num/len(name_pairs)))
    
    return Pc

def testBayes(Pc, name, regions, name_pairs, c1=1, c2=0.7, c3=1.5):
    grams = getGrams(name)
    
    scores = [np.zeros(len(regions)) for i in range(3)] # 3 * num of regions
    for N in range(3):
        data = getNgrams(N+1, name_pairs, regions)
        for rid in range(len(regions)):
            tot = sum(data[rid].values())
            voc = len(data[rid].keys())
            const = math.log(tot + voc)
        
            scores[N][rid] = Pc[rid]
            for gram in grams[N]:
                if gram in data[rid].keys():
                    # print(gram)
                    scores[N][rid] += math.log(data[rid][gram]+1) - const
                else:
                    scores[N][rid] -= const

    score = c1*scores[0] + c2*scores[1] + c3*scores[2]
    return score

if __name__ == '__main__':
    Pc = getPc()
    regions, name_pairs = readData()
    name = input("Type your name here (enter '#' to quit): ").lower()
    while name != "#":
        score = testBayes(Pc, name.lower(), regions, name_pairs)
        sort_arg = score.argsort()[::-1]
        for i in range(5):
            print("No.%d: %s, %f"%(i+1, regions[sort_arg[i]][0], (score[sort_arg[i]])))
        name = input("Type your name here (enter '#' to quit): ").lower()
    





    