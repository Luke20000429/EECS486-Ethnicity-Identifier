f = open("nation_names.csv","r")
allNations2Comb = dict() 
seqCombId = []
combNationStr = []
for line in f:
    n_c = line[:-1].lower().replace(" ","").split(",")
    flag = 1
    for i in range(len(combNationStr)):
        if combNationStr[i] == n_c[1]:
            flag = 0
            allNations2Comb[n_c[0]] = i
            seqCombId.append(i)
            break

    if flag:
        allNations2Comb[n_c[0]] = len(combNationStr)
        seqCombId.append(len(combNationStr))
        combNationStr.append(n_c[1])

f.close()

print(seqCombId)
print(allNations2Comb)

