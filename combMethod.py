import Levenshtein
import os.path as pt
import numpy as np
import ctypes
import sys
import random
lib = ctypes.cdll.LoadLibrary
prepostfix = None
if (sys.platform == 'win32'):
    prepostfix = lib('./prepostfix.dll') #C++ dynamic library to calculate similarity between strings quickly
else:
    prepostfix = lib('./prepostfix.so') #C++ dynamic library to calculate similarity between strings quickly


class EthnicityPredictor():
    def __init__(self, _mode=0):
        if (sys.platform == 'win32'):
            self.prepostfix = lib('./prepostfix.dll') #C++ dynamic library to calculate similarity between strings quickly
        else:
            self.prepostfix = lib('./prepostfix.so') #C++ dynamic library to calculate similarity between strings quickly

        self.popNation = np.array([5,1,6,2,20,18,7,20,1,0.2,13,0.1,0.2])  # temp setting
        self.mode = _mode
        self.sample_factor = 100

    def refresh(self, _mode=None):
        if _mode:
            self.mode = _mode
        self.hit = [0]*10
        self.miss = [0] * 10
        self.hitna = np.array([0] * self.countryNum)
        self.missna = np.array([0] * self.countryNum)
        self.line_num = 0
        self.preposthit = 0 # hit time for prediction using prefix and suffix
        self.prepostmiss = 0

    def readData(self, sample=None, nationINFO='data/regions.txt', nameINFO='data/redb.txt', testINFO='data/test_set.txt'):
        
        nations = []
        name_pairs = []

        with open(nationINFO, 'r', encoding='utf-8') as f:  # get nation names
            for line in f:
                nation = line[:-1]
                nations.append(nation)

        test_set = [[] for _ in nations]
        self.countryNum = len(nations)

        with open(nameINFO, 'r', encoding='utf-8') as f: # get training name pairs
            for line in f:
                na_na = line[:-1].split(" ")
                na_na[1] = int(na_na[1])
                name_pairs.append(tuple(na_na))

        if sample and (sample < len(name_pairs)):
            name_pairs = random.sample(name_pairs, sample);

        with open(testINFO, "r", encoding='utf-8') as f:
            for line in f:
                na_na = line[:-1].split('#')
                names = na_na[0]
                nation = int(na_na[1])
                test_set[nation].append(names)

        self.nations = nations
        self.pairs = name_pairs
        self.test_set = test_set

        self.refresh()

        return nations, name_pairs, test_set

    # count name and nation pairs
    def countNN(self, smoothingNum = 1):
        retDict = dict()
        numForNation = np.array([smoothingNum] * self.countryNum)
        numSingleNameNation = np.array([0] * self.countryNum)
        setpre = dict() # a map from the first two characters to the names
        setpost = dict() #a map from the last two characters to the names
        
        for x, nt in self.pairs:
            if x not in retDict:
                retDict[x] = np.array([0] * self.countryNum)
            if x[:2] not in setpre:
                setpre[x[:2]] = set()
            if x not in setpre[x[:2]]:
                setpre[x[:2]].add(x)
            if x[-2:] not in setpost:
                setpost[x[-2:]] = set()
            if x not in setpost[x[-2:]]:
                setpost[x[-2:]].add(x)
            
            retDict[x][nt] += 1
            numForNation[nt] += 1
        
        for nm, retDictnm in retDict.items():
            if sum(retDictnm) == 1: # name that only appear once
                numSingleNameNation += retDictnm
            correctedCount = retDictnm / numForNation
            retDict[nm] = correctedCount / sum(correctedCount)
        
        notFoundNameRatio = numSingleNameNation / numForNation # to find P(nation | name not found in the database)

        print(notFoundNameRatio)
        print("------------")

        self.nameBase = retDict
        self.setpre = setpre
        self.setpost = setpost
        self.notFoundNameRatio = notFoundNameRatio

        return retDict, setpre, setpost, notFoundNameRatio

    def test(self, names, target, mode=0):
        # method :
        # 0 pre/suffix
        # 1 ngram bayes
        # 2 combine 0\1
        p = self.popNation

        inbase = 0
        for name in names:
            
            if name in self.nameBase:
                # found in database
                inbase += 1
                p = p * (self.nameBase[name] + 0.1 / 13)  # 0.1 / countryNum=13 is for smoothing
            elif mode == 0:
                ret = np.array([len(self.nameBase)/100] * self.countryNum)
                if len(name) >= 2:
                    setprenames = set()
                    if self.setpre.__contains__(name[:2]):
                        setprenames = self.setpre[name[:2]]
                    setpostnames = set()
                    if self.setpost.__contains__(name[-2:]):
                        setpostnames = self.setpost[name[-2:]]

                    for trainName in (setprenames or setpostnames): # only consider names in the database that shares the first / last two characters
                        scores = self.nameBase[trainName] # probability of nations
                        simSco = prepostfix.prepostsqr(bytes(name, encoding="utf-8"), bytes(trainName, encoding="utf-8")) # calculate similarity score
                        ret = ret + simSco * scores

                ret = ret * self.notFoundNameRatio # add the factor P(nation | name not found in the database)
                ret = ret / sum(ret)
                p = p * ret
                if ret.argmax() == target:
                    self.preposthit += 1
                else:
                    self.prepostmiss += 1
                # print(name + ": " + nations[ret.argmax()])

            elif mode == 1:

                pass
            elif mode == 2:

                pass

        p = p / sum(p)
        # print (p)
        # print(line + ": " + nations[p.argmax()])
        # print(p.argmax())
        if p.argmax() == target:
            # print("Hit")
            self.hit[inbase] += 1
            self.hitna[target] += 1
        else:
            # print("Miss")
            self.miss[inbase] += 1
            self.missna[target] += 1

        return p

    def Run(self):

        self.readData()
        self.countNN()

        print("ready!\n")

        for nation_id in range(self.countryNum):
            nation = self.nations[nation_id]
            print("predicting %s\n"%nation)
            # sample names in proportion to the population
            # names = random.sample(self.test_set[nation_id], int(self.popNation[nation_id] * self.sample_factor))
            names = self.test_set[nation_id][: int(self.popNation[nation_id] * self.sample_factor)]
            for name in names:
                parts = name.split()
                self.test(parts, nation_id)

        print(self.hitna/(self.hitna + self.missna))
        print("HIT NUM for match nums: " + str(self.hit))
        print("MISS NUM for match nums: " + str(self.miss))
        print("HIT RATE: " + str(sum(self.hit) / (sum(self.miss) + sum(self.hit))))

        return

        
if __name__ == '__main__':
    ep = EthnicityPredictor()

    ep.Run()


    