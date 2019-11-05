import numpy as np
import pandas as pd
from itertools import combinations,chain

global suppcount
suppcount = {}


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)))

def listToString(s):   
    str1 = " " 
    return (str1.join(s)) 

def getDataSet(filename,N):
    datafile = open(filename, "r")
    dataset = datafile.read().splitlines()[:N]
    for index,transaction in enumerate(dataset):
        if(transaction.strip() == ''):
                continue
        dataset[index] = transaction.split(" ")
        dataset[index] = frozenset(int(numeric_string) for numeric_string in dataset[index])
    datafile.close()
    return dataset

def getAttributes():
    attributes = pd.read_excel('OnlineRetailAtrributes.xlsx',header = None)
    attributes = attributes.set_index(1).T.to_dict('list')
    for item in attributes:
        attributes[item][0] = attributes[item][0].replace("'","")
        attributes[item] = listToString(attributes[item])
    return attributes

def getFrequency(dataset,combinations):
    L1 = {}
    for transaction in dataset:
        for itemset in combinations:
            itemset = frozenset(itemset)
            if(itemset.issubset(transaction)):
                if(itemset in L1):
                    L1[itemset] = L1[itemset] + 1
                else:
                    L1[itemset] = 1
    return L1

def generateCombinations(attributes,level):
    comb = combinations(attributes, int(level))
    return list(comb)

def candidatesElimination(dataset,candidates,minsupp,level,oldresult):
    global frequent
    frequent = set()
    global result
    result = []
    for item in candidates.keys():        
      if(candidates[item] >= minsupp):
            result.append(item)
            suppcount[item] = candidates[item]
            for i in item:
                frequent.add(i)
    if(len(result) == 0):
        result = set(oldresult)
    else:
        print(frequent)
        oldresult = result
        candidatesElimination(dataset,getFrequency(dataset,generateCombinations(frequent,level+1)),minsupp,level+1,oldresult)
    return result   

def generateSupportCount(result):
    for s in list(suppcount):
        flag = False
        for r in result:
            if(s.issubset(r)):
                flag = True
        if(flag  == False):
            del suppcount[s]

def generateAssociationRules(result,minconf):
    for r in result:
        x = list(powerset(r))
        for set_ in x:
            set_ = frozenset(set_)
            for set1 in x:
                set1 = frozenset(set1)
                if(set1.isdisjoint(set_)):
                    conf = calculateConfidence(set_,set1)
                    if(conf >= minconf):
                        print(set_,"-->",set1,conf)

def calculateConfidence(antecedent,consequent):
    support = float(suppcount[antecedent.union(consequent)])
    return float(support/suppcount[antecedent])

def apriori(filepath,datapercentage,minsupp,minconf):
    level = 1
    numberoflines = int((541909*(datapercentage/100)))
    dataset = []
    dataset = getDataSet(filepath,numberoflines)
    print(len(dataset))
    attributes = getAttributes()
    comb = generateCombinations(attributes,level)
    frequency = getFrequency(dataset,comb)
    result = candidatesElimination(dataset,frequency,minsupp,level,{}) 
    print(result)
    generateSupportCount(result)
    print(suppcount)
    generateAssociationRules(result,minconf)