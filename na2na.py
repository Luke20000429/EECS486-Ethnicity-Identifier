import Levenshtein
import numpy as np

def readData(nationINFO='nations.txt', nameINFO='db.txt'):

    nations = []
    name_pairs = []

    with open(nationINFO, 'r', encoding='utf-8') as f:
        for line in f:
            nation = line[:-1]
            nations.append(nation)
            

    with open(nameINFO, 'r', encoding='utf-8') as f:
        for line in f:
            na_na = line[:-1].split(" ")
            na_na[1] = int(na_na[1])
            name_pairs.append(tuple(na_na))

    return nations, name_pairs


def calcStrSimSoc(str1, str2):
    return 1/(1.05-Levenshtein.ratio(str1, str2)) - 1/1.06


def countNN(pairs, countryNum, smoothingNum = 3):
    retDict = dict()
    for x, nt in pairs:
        if x not in pairs:
            retDict[x] = np.array([smoothingNum] * countryNum)
        retDict[x][nt] += 1
    
    for nm in retDict:
        retDict[nm] = retDict[nm]/sum(retDict[nm])
        
    return retDict

def main():
    # print(nameBase)
    nations, name_pairs = readData()
    countryNum = len(nations)
    nameBase = countNN(name_pairs, countryNum)
    print("ready!\n")
    name = input("Type your name here (enter 'q' to quit): ").lower()
    while name != "q":
        if name in nameBase:
            print(nations[nameBase[name].argmax()])
        else:
            ret = np.array([0] * countryNum)
            for trainName, scores in nameBase.items():
                ret = ret + calcStrSimSoc(name, trainName) * scores
            ret = ret / sum(ret)
            print(nations[ret.argmax()])

        
if __name__ == '__main__':
    main()
    