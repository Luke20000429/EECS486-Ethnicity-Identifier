import Levenshtein
import os.path as pt
import numpy as np
import ctypes
import random
# import matplotlib
lib = ctypes.cdll.LoadLibrary
prepostfix = lib('./prepostfix.dll') #C++ dynamic library to calculate similarity between strings quickly

# combDict = {'american': 0, 'greek': 1, 'french': 2, 'english': 3, 'russian': 4, 'german': 5, 'macedonian': 6, 'japanese': 7, 'canadian': 8, 'british': 9, 'iranian': 10, 'mexican': 11, 'italian': 12, 'indian': 13, 'pakistani': 14, 'afghan': 15, 'portuguese': 16, 'norwegian': 17, 'iraqi': 18, 'austrian': 19, 'hungarian': 20, 'dutch': 21, 'australian': 22, 'saudi': 23, 'chilean': 24, 'welsh': 25, 'irish': 26, 'egyptian': 27, 'lithuanian': 28, 'latvian': 29, 'burmese': 30, 'israeli': 31, 'belgian': 32, 'ukrainian': 33, 'chinese': 34, 'romanian': 35, 'colombian': 36, 'armenian': 37, 'peruvian': 38, 'argentine': 39, 'nicaraguan': 40, 'bulgarian': 41, 'albanian': 42, 'syriac': 43, 'basque': 44, 'serb': 45, 'catalan': 46, 'moroccan': 47, 'syrian': 48, 'libyan': 49, 'czech': 50, 'ugandan': 51, 'ghanaian': 52, 'kenyan': 53, 'estonian': 54, 'zambian': 55, 'georgian': 56, 'slovak': 57, 'tamil': 58, 'cambodian': 59, 'brazilian': 60, 'dominican': 61, 'korean': 62, 'vietnamese': 63, 'nigerian': 64, 'palestinian': 65, 'lebanese': 66, 'tunisian': 67, 'cuban': 68, 'slovene': 69, 'ethiopian': 70, 'congolese': 71, 'emirati': 72, 'venezuelan': 73, 'somali': 74, 'taiwanese': 75, 'montenegrin': 76, 'panamanian': 77, 'singaporean': 78, 'salvadoran': 79, 'jamaican': 80, 'mozambican': 81, 'haitian': 82, 'belarusian': 83, 'namibian': 84, 'tibetan': 85, 'bermudian': 86, 'azerbaijani': 87, 'jordanian': 88, 'yemeni': 89, 'barbadian': 90, 'burkinab√©': 91, 'surinamese': 92, 'senegalese': 93, 'filipino': 94, 'malaysian': 95, 'malagasy': 96, 'guinean': 97, 'bolivian': 98, 'indonesian': 99, 'paraguayan': 100, 'guatemalan': 101, 'chadian': 102, 'breton': 103, 'algerian': 104, 'bosniak': 105, 'thai': 106, 'manx': 107, 'nauruan': 108, 'burundian': 109, 'honduran': 110, 'lao': 111, 'nepalese': 112, 'maltese': 113, 'bahamian': 114, 'uruguayan': 115, 'bangladeshi': 116, 'belizean': 117, 'ecuadorian': 118, 'cypriot': 119, 'faroese': 120, 'grenadian': 121, 'liberian': 122, 'kazakh': 123, 'cameroonian': 124, 'mauritian': 125, 'equatoguinean': 126, 'angolan': 127, 'tongan': 128, 'maldivian': 129, 'sudanese': 130, 'qatari': 131, 'nigerien': 132, 'rwandan': 133, 'finn': 134, 'guyanese': 135, 'samoan': 136, 'mongolian': 137, 'tanzanian': 138, 'mauritanian': 139, 'gibraltarian': 140, 'moldovan': 141, 'swazi': 142, 'botswana': 143, 'bahraini': 144, 'beninese': 145, 'bhutanese': 146, 'comorian': 147, 'djiboutian': 148, 'gambian': 149, 'i-kiribati': 150, 'malian': 151, 'marshallese': 152, 'omani': 153, 'sammarinese': 154, 'vanuatuan': 155, 'tuvaluan': 156, 'gabonese': 157, 'sotho': 158, 'aruban': 159, 'uzbek': 160, 'malawian': 161, 'togolese': 162, 'kyrgyz': 163, 'kuwaiti': 164, 'bruneian': 165, 'tajik': 166, 'eritrean': 167, 'palauan': 168, 'andorran': 169, 'turk': 170, 'vincentian': 171, 'dane': 172, 'arabs': 173, 'polish': 174, 'scottish': 175, 'spanish': 176}
# combIDs = [0, 1, 2, 3, 2, 2, 2, 4, 0, 3, 5, 6, 2, 7, 5, 5, 6, 8, 5, 2, 2, 2, 0, 5, 6, 3, 3, 5, 2, 2, 4, 9, 2, 2, 4, 2, 6, 2, 6, 6, 6, 2, 2, 5, 6, 2, 2, 5, 5, 5, 2, 10, 10, 10, 2, 10, 5, 2, 7, 4, 6, 6, 4, 4, 10, 5, 5, 5, 6, 2, 10, 10, 5, 6, 5, 4, 2, 6, 4, 6, 6, 6, 10, 2, 10, 4, 11, 12, 5, 5, 13, 11, 6, 10, 6, 4, 6, 10, 6, 4, 6, 6, 10, 3, 5, 2, 4, 3, 13, 10, 6, 7, 7, 2, 13, 6, 5, 6, 6, 5, 2, 13, 10, 5, 10, 10, 10, 6, 10, 7, 5, 5, 10, 10, 8, 6, 13, 4, 10, 10, 11, 2, 10, 10, 5, 10, 7, 10, 10, 10, 11, 10, 13, 5, 2, 13, 13, 10, 10, 8, 5, 10, 10, 14, 5, 14, 14, 10, 13, 2, 5, 10, 8, 5, 2, 3, 6]
popNation = np.array([5,1,6,2,20,18,7,20,1,0.2,13,0.1,0.2])  # temp setting
def readData(nationINFO='data/regions.txt', nameINFO='data/redb.txt'):

    nations = []
    name_pairs = []

    with open(nationINFO, 'r', encoding='utf-8') as f:  # get nation names
        for line in f:
            nation = line[:-1]
            nations.append(nation)

    with open(nameINFO, 'r', encoding='utf-8') as f:  # get training name pairs
        iter = 0
        for line in f:
            na_na = line[:-1].split(" ")
            na_na[1] = int(na_na[1])
            name_pairs.append(tuple(na_na))

    # return nations, random.sample(name_pairs, k=2000000)
    return nations, name_pairs
# count name and nation pairs
def countNN(pairs, countryNum, smoothingNum = 1):
    retDict = dict()
    numForNation = np.array([smoothingNum] * countryNum)
    numSingleNameNation = np.array([0] * countryNum)
    setpre = dict() # a map from the first two characters to the names
    setpost = dict() #a map from the last two characters to the names
    
    for x, nt in pairs:
        if x not in retDict:
            retDict[x] = np.array([0] * countryNum)
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
    return retDict, setpre, setpost, notFoundNameRatio

def main():
    # print(nameBase)
    nations, name_pairs = readData()
    countryNum = len(nations)
    nameBase, setpre, setpost, notFoundNameRatio = countNN(name_pairs, countryNum)
    print("ready!\n")
    print(len(nameBase))
    f = open("data/test_set.txt","r", encoding='utf-8')
    hit = [0]*10
    miss = [0] * 10
    hitna = np.array([0] * countryNum)
    missna = np.array([0]*countryNum)
    line_num = 0
    target_count = [0] * countryNum
    preposthit = 0 # hit time for prediction using prefix and suffix
    prepostmiss = 0

    # testing
    for line in f:
        # line_num += 1
        # if line_num % 10 != 0:
        #     continue
        nameParts_and_target = line.split()
        target = int(nameParts_and_target[-1][1:])
        if target_count[target] > popNation[target] * 100: # make sure that the test set is in proportion with the population ratio
            continue
        target_count[target] += 1
        nameParts = nameParts_and_target[:-1]

        p = popNation # initialize the probability for each region as their population
        inbasenum = 0
        for name in nameParts:
            if name in nameBase:
                inbasenum += 1
                # print("found in database")
                p = p * (nameBase[name] + 0.1 / countryNum)  # 0.1 / countryNum is for smoothing
                # print(name + ": " + nations[nameBase[name].argmax()])
            else:
                ret = np.array([len(nameBase)/100] * countryNum)
                if len(name) >= 2:
                    setprenames = set()
                    if setpre.__contains__(name[:2]):
                        setprenames = setpre[name[:2]]
                    setpostnames = set()
                    if setpost.__contains__(name[-2:]):
                        setpostnames = setpost[name[-2:]]

                    for trainName in (setprenames or setpostnames): # only consider names in the database that shares the first / last two characters
                        scores = nameBase[trainName] # probability of nations
                        simSco = prepostfix.prepostsqr(bytes(name,encoding="utf-8"), bytes(trainName,encoding="utf-8")) # calculate similarity score
                        ret = ret + simSco * scores

                ret = ret * notFoundNameRatio # add the factor P(nation | name not found in the database)
                ret = ret / sum(ret)
                p = p * ret
                # sol = ret.argmax()
                # if sol == target:
                #     preposthit += 1
                # else:
                #     prepostmiss += 1
                # print(name + ": " + nations[ret.argmax()])
        
        p = p / sum(p)
        # print (p)
        # print(line + ": " + nations[p.argmax()])
        # print(p.argmax())
        if p.argmax() == target:
            # print("Hit")
            hit[inbasenum] += 1
            hitna[target] += 1
        else:
            # print("Miss")
            miss[inbasenum] += 1
            missna[target] += 1
    print(target_count)
    print("Total test size: " + str(sum(target_count)))
    print(hitna/(hitna + missna))
    print("HIT NUM for match nums: " + str(hit))
    print("MISS NUM for match nums: " + str(miss))
    print("HIT RATE: " + str(sum(hit) / (sum(miss) + sum(hit))))
    # print(preposthit/prepostmiss)
    # print("MISS NUM: " + str(miss))
    # nameInput = ""
    # while nameInput != "q":
    #     nameInput = input("Type your name here (enter 'q' to quit): ").lower()
    #     nameParts = nameInput.split(" ")
    #     p = [1] * countryNum
    #     for name in nameParts:
    #         if name in nameBase:
    #             print("found in database")
    #             p = p * (nameBase[name] + 0.1 / countryNum)
    #             print(name + ": " + nations[nameBase[name].argmax()])
    #         else:
    #             ret = np.array([1] * countryNum)
    #             for trainName, scores in nameBase.items():
    #                 simSco = prepostfix.prepostsqr(name, trainName)
    #                 # if simSco > 0.2:
    #                 ret = ret + simSco * scores
    #             ret = ret / sum(ret)
    #             p = p * ret
    #             print(name + ": " + nations[ret.argmax()])
        
        # p = p / sum(p)
        # print (p)
        # print(nameInput + ": " + nations[p.argmax()])
        
if __name__ == '__main__':
    main()
    