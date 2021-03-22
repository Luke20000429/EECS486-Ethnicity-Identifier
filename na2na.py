import Levenshtein
import numpy as np
countryNum = 2
countryName = ["ch","us"]

def calcStrSimSoc(str1, str2):
    return 1/(1.05-Levenshtein.ratio(str1, str2)) - 1/1.06


def countNN(pairs, smoothingNum = 3):
    retDict = dict()
    for x, nt in pairs:
        if x not in pairs:
            retDict[x] = np.array([smoothingNum] * countryNum)
        retDict[x][nt] += 1
    
    for nm in retDict:
        retDict[nm] = retDict[nm]/sum(retDict[nm])
        
    return retDict

def genNameBase():
    pairs = [("alice", 0), ("bob", 0), ("wang", 1), ("zhou", 1)]
    return countNN(pairs)

def testName(name, nameBase):
    print(nameBase)
    if name in nameBase:
        return nameBase[name]
    else:
        ret = np.array([0] * countryNum)
        for trainName, scores in nameBase.items():
            ret = ret + calcStrSimSoc(name, trainName) * scores
        ret = ret / sum(ret)
        return ret

print(testName("who", genNameBase()))