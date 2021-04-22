"""This program aids to turn the data in NameNationality.txt into format we want"""
import csv

def main():
    # turn the 3-letter nationality into ethnicity
    nation_nationality_dict = {} # country nams -> nationality
    with open('data/demonyms.csv','r') as fid:
        csv_reader = csv.reader(fid)
        for item in csv_reader:
            if item[1].lower() not in nation_nationality_dict:
                nation_nationality_dict[item[1].lower()] = []
            nation_nationality_dict[item[1].lower()].append(item[0].lower())
    
    ethinity_dict = {} #nationality -> ethnicity
    with open('data/nation-region.txt', 'r') as fid:
        for line in fid.readlines():
            nation = line.split(',')[0]
            ethinity_dict[nation] = line.split(',')[1].rstrip('\n')
    
    region_id_dict = {} # ethnicity -> ethnicity ID
    with open('data/regions.txt', 'r') as fid:
        id = 0
        for line in fid.readlines():
            region = line.split(' ')[0]
            region_id_dict[region] = id
            id += 1
            
    code_region_dict = {} # 3-letter country acronyms -> country names
    with open('data/NationDict.txt', 'r') as fid:
        for line in fid.readlines():
            abbr = line.split('\t')[0]
            nation = line.split('\t')[1].rstrip('\n').lower()
            if nation not in nation_nationality_dict:
                continue
            nationalitys = nation_nationality_dict[nation]
            flag = False
            ethinity = ''
            for nationality in nationalitys:
                if nationality in ethinity_dict:
                    ethinity = ethinity_dict[nationality]
            if not ethinity:
                continue
            code_region_dict[abbr] = region_id_dict[ethinity]
            
        with open('data/olym.txt', 'w') as output:
            with open('data/NameNationality', 'r') as input:
                for line in input.readlines():
                    name = line.split('\t')[0]
                    nationality = line.split('\t')[1]
                    flag_length = False
                    for part in name.split(' '):
                        if part == '':
                            continue
                        if len(part) < 3:
                            flag_length = True
                    if flag_length:
                        continue
                    for n in nationality.split(' '):
                        if n not in code_region_dict:
                            continue
                        code = code_region_dict[n]
                        output.write(f'{name.lstrip().lower()} #{code}\n')
            

if __name__ == '__main__':
    main()