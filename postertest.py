import os.path as pt
import numpy as np
import ctypes
import sys
import random
import math
import codecs
import csv
from ngram import getNgrams, getGrams
from combMethod import EthnicityPredictor as EP
lib = ctypes.cdll.LoadLibrary

printNames = ["USA/Canada/Australia", "Greek", "European","Celtic English","East Asian", "Muslim","Hispanic","South Asian","Nordic","Jewish","African","Others","Oceania"]

class PosterPredicter(EP):

    def PrePost(self, name):

        # run prefix-suffix model
    
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
        if self.mode == 3:
            ret = ret * self.notFoundNameRatio # add the factor P(nation | name not found in the database)
        ret = ret / sum(ret)

        return np.log(ret)

    def Bayes(self, name, c1=0.025, c2=0.05, c3=0.25):

        # Run naive bayes model 

        grams = getGrams(name)
        scores = [np.zeros(self.countryNum) for i in range(3)] # 3 * num of regions
        for N in range(3):
            data = self.ngrams[N]
            for rid in range(self.countryNum):
                tot = sum(data[rid].values())
                voc = len(data[rid].keys())
                const = math.log(tot + voc)
            
                scores[N][rid] = 0
                for gram in grams[N]:
                    if gram in data[rid].keys():
                        # print(gram)
                        scores[N][rid] += math.log(data[rid][gram]+1) - const
                    else:
                        scores[N][rid] -= const

        score = c1*scores[0] + c2*scores[1] + c3*scores[2]

        return score
    
    def predict(self, names):

        # predict ethnicity of a name

        # method :
        # 0 pre/suffix
        # 1 ngram bayes
        # 2 combine 0\1
        p = self.Pc

        inbase = 0
        for name in names.split():
            self.nametest += 1
            # print(name)
            if name in self.nameBase:
                
                self.namefind += 1
                # found in database
                inbase += 1
                p = p + np.log(self.nameBase[name] + 0.1 / 13)  # 0.1 / countryNum=13 is for smoothing
            else:
                # print("not in database, using prepostffix")
                if self.mode == 0 or self.mode == 2 or self.mode == 3:
                    p = p + self.PrePost(name)

                if self.mode == 1 or self.mode == 2 or self.mode == 3:
                # print("not in database, using bayes")
                    p = p + self.Bayes(name)

        print(printNames[p.argmax()], end=' ')
        
        numpp = np.array(p)
        numppn = numpp - max(numpp)
        expp = [math.exp(p) for p in numppn]
        certainty = max(expp)/sum(expp)
        print(str(round(certainty*100))+'%')

        return p.argmax()

    def Run(self):

        # keep receiving names and do prediction

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
        elif self.mode == 3:
            print("Launch ethnity predictor with combined mode + no-match weight")
            self.countCate()

        print("ready!\n")
        testname = ""
        while testname != "stop":
            testname = input("Please enter a name (enter 'stop' to exit): ")
            self.predict(str.lower(testname))
        
        return


    def Run_sports_player_test(self):

        # run the test in our report on sports players

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
        elif self.mode == 3:
            print("Launch ethnity predictor with combined mode + no-match weight")
            self.countCate()

        print("ready!\n")
        f_go = open("data/chess_players.txt", 'r')
        cnt = [0] * self.countryNum
        for testname in f_go:
            # testname = input("Please enter a name (enter 'stop' to exit): ")
            cnt[self.test(str.lower(testname))] += 1
        
        f_go.close()
        print(cnt)
        return

        
if __name__ == '__main__':

    # run the demo
    print("Initializing...")
    pp = PosterPredicter(_mode=3)
    # mode should be combined mode (mode 3)
    pp.Run()




    