import Levenshtein
import os.path as pt
import numpy as np
import ctypes
import sys
import random
import math
from ngram import getNgrams, getGrams
lib = ctypes.cdll.LoadLibrary

class EthnicityPredictor():
    def __init__(self, _mode=0):
        if sys.platform == 'win32':
            self.prepostfix = lib('./prepostfix.dll') #C++ dynamic library to calculate similarity between strings quickly
        elif sys.platform == 'linux':
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
        self.bayeshit = 0
        self.bayesmiss = 0

        self.namefind = 0
        self.nametest = 0

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

    def countNN(self, smoothingNum = 1):
        # count name and nation pairs
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

        self.Pc = np.log(self.popNation/self.popNation.sum())

        return retDict, setpre, setpost, notFoundNameRatio

    def countCate(self):
        # get grams data and P_category
        self.ngrams = []
        for N in range(3):
            self.ngrams.append(getNgrams(N+1, self.pairs, self.nations))

        return self.ngrams

    def testPrePost(self, name, target):

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
                simSco = self.prepostfix.prepostsqr(bytes(name, encoding="utf-8"), bytes(trainName, encoding="utf-8")) # calculate similarity score
                ret = ret + simSco * scores
        ret = ret * self.notFoundNameRatio # add the factor P(nation | name not found in the database)
        ret = ret / sum(ret)

        if ret.argmax() == target:
            self.preposthit += 1
        else:
            self.prepostmiss += 1
        
        return np.log(ret)

    def testBayes(self, name, target, c1=0.2, c2=0.7, c3=1.5):
        grams = getGrams(name)
    
        scores = [np.zeros(self.countryNum) for i in range(3)] # 3 * num of regions
        for N in range(3):
            data = self.ngrams[N]
            for rid in range(self.countryNum):
                tot = sum(data[rid].values())
                voc = len(data[rid].keys())
                const = math.log(tot + voc)
            
                scores[N][rid] = self.Pc[rid]
                for gram in grams[N]:
                    if gram in data[rid].keys():
                        # print(gram)
                        scores[N][rid] += math.log(data[rid][gram]+1) - const
                    else:
                        scores[N][rid] -= const

        score = c1*scores[0] + c2*scores[1] + c3*scores[2]
        if score.argmax() == target:
            self.bayeshit += 1
        else:
            self.bayesmiss += 1
        return score+100
        
    def test(self, names, target):
        # method :
        # 0 pre/suffix
        # 1 ngram bayes
        # 2 combine 0\1
        p = self.Pc

        inbase = 0
        for name in names:
            self.nametest += 1
            if name in self.nameBase:
                self.namefind += 1
                # found in database
                inbase += 1
                p = p + np.log(self.nameBase[name] + 0.1 / 13)  # 0.1 / countryNum=13 is for smoothing
            elif self.mode == 0:
                # print("not in database, using prepostffix")
                p = p + self.testPrePost(name, target)

            elif self.mode == 1:
                # print("not in database, using bayes")
                p = p + self.testBayes(name, target)
                
            elif self.mode == 2:

                pass

        if p.argmax() == target:
            # print("Hit")
            self.hit[inbase] += 1
            return True
        else:
            # print("Miss")
            self.miss[inbase] += 1
            return False

    def Run(self):

        self.readData()
        self.countNN()
        if self.mode == 0:
            print("Launch ethnity predictor with pre\suffix classifier mode")
        elif self.mode == 1:
            print("Launch ethnity predictor with ngram bayes classifier mode")
            self.countCate()
        elif self.mode == 2:
            print("Launch ethnity predictor with combined mode")
            self.countCate()

        print("ready!\n")

        for nation_id in range(self.countryNum):
            nation = self.nations[nation_id].split()[0]
            print("predicting %s"%nation)
            # sample names in proportion to the population
            # names = random.sample(self.test_set[nation_id], int(self.popNation[nation_id] * self.sample_factor))
            names = self.test_set[nation_id][: int(self.popNation[nation_id] * self.sample_factor)]
            for name in names:
                parts = name.split()
                if self.test(parts, nation_id):
                    self.hitna[nation_id] += 1
                else:
                    self.missna[nation_id] += 1

            print("accuracy %f\n------------"%(self.hitna[nation_id]/(self.hitna[nation_id]+self.missna[nation_id])))


        if self.mode == 0:
            # print("HIT NUM for match nums: " + str(self.hit))
            # print("MISS NUM for match nums: " + str(self.miss))
            print("Hit rate of pure prepostffix: %f"%(self.preposthit/(self.preposthit+self.prepostmiss)))
        elif self.mode == 1:
            print("Hit rate of pure bayes: %f"%(self.bayeshit/(self.bayeshit+self.bayesmiss)))

        print("name find rate: %f"%(self.namefind/self.nametest))
        print("Total accuracy: " + str(sum(self.hitna) / (sum(self.missna) + sum(self.hitna))))

        return

        
if __name__ == '__main__':
    ep = EthnicityPredictor(_mode=0)
    # method :
        # 0 pre/suffix
        # 1 ngram bayes
        # 2 combine 0\1
    
    ep.Run()


    