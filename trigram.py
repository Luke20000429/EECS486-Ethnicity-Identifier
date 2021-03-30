import os
import sys
import codecs
import math
import numpy as np

def readData(nationINFO='regions.txt', nameINFO='redb.txt'):
    
    nations = []
    name_pairs = []

    with open(nationINFO, 'r', encoding='utf-8') as f:
        for line in f:
            nation = line[:-1]
            nations.append(nation) ## #line:nation_id nation
            

    with open(nameINFO, 'r', encoding='utf-8') as f:
        for line in f:
            na_na = line[:-1].split(" ")
            na_na[1] = int(na_na[1])
            name_pairs.append(tuple(na_na)) ## name nation_id

    return nations, name_pairs

def trainBigramLanguageModel(bidicts, chardicts, pair):
    name, nation = pair
    if name[0] in chardicts[nation].keys():
        chardicts[nation][name[0]] += 1
    else:
        chardicts[nation][name[0]] = 1
    
    for i in range(1, len(name)):
        bi = name[i-1:i+1]
        char = name[i]
        if char in chardicts[nation].keys():
            chardicts[nation][char] += 1
        else:
            chardicts[nation][char] = 1
        if bi in bidicts[nation].keys():
            bidicts[nation][bi] += 1
        else:
            bidicts[nation][bi] = 1

    return bidicts, chardicts

def identityNation(name, nations, bidicts, chardicts):
    P = np.ones(len(nations))
    for nid in range(len(nations)):
        V = len(chardicts[nid].keys())
        total = sum(chardicts[nid].values())
        if total > 0:
            if name[0] in chardicts[nid].keys():
                P[nid] = math.log((chardicts[nid][name[0]]+1)/(total + V))
            else:
                P[nid] = math.log(1/(total + V))
            for i in range(1, len(name)):
                C1 = 0
                C12 = 0
                if name[i-1:i+1] in bidicts[nid].keys():
                    C12 = bidicts[nid][name[i-1:i+1]]
                    C1 = chardicts[nid][name[i-1]]
                elif name[i-1] in chardicts[nid].keys():
                    C1 = chardicts[nid][name[i-1]]
                P[nid] += math.log((C12 + 1)/(C1 + V))
        else:
            P[nid] = -9999
    
    print(P.max())
    return nations[P.argmax()]

def train():
    
    nations, name_pairs = readData()
    bidicts = [dict() for i in nations]
    chardicts = [dict() for i in nations]
    for pair in name_pairs:
        bidicts, chardicts = trainBigramLanguageModel(bidicts, chardicts, pair)
    return nations, bidicts, chardicts

if __name__ == '__main__':
    nations, bidicts, chardicts = train()
    name = input("Type your name here (enter '#' to quit): ").lower()
    while name != "#":
        print(identityNation(name, nations, bidicts, chardicts))
        name = input("Type your name here (enter '#' to quit): ").lower()

    
