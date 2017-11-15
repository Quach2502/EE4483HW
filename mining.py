import string
from collections import defaultdict
from itertools import chain, combinations

def getTransactionList(filename):
    transactionList = []
    for l in open(filename,'rU'):
        transactionList.append([item.translate(string.maketrans('\n',' ')).strip() for item in l.split(',')])
    return [frozenset(record) for record in transactionList]

def getItemSet(transactionList):
    itemSet = set()
    for transaction in transactionList:
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet

def generateCandidate(itemSetL, k):
    return set([i.union(j) for i in itemSetL for j in itemSetL if len(i.union(j)) == k])

def scan(transactionList, candidateSet, minSupport,freqSet):
    localSet = defaultdict(int)
    Lset = set()
    for candidate in candidateSet:
        for transaction in transactionList:
            if candidate.issubset(transaction):
                localSet[candidate] += 1
                freqSet[candidate] += 1
    for candidate, cnt in localSet.items():
        support = float(cnt)/len(transactionList)
        if support >= minSupport:
            Lset.add(candidate)
    return Lset

def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def apriori(transactionList, minSupport, minConf):
    freqSet = defaultdict(int)
    largeSet =  dict()
    assocRules = list()
    interestingRules = list()
    itemSet = getItemSet(transactionList)
    C_set_1 = scan(transactionList,itemSet,minSupport,freqSet)
    current_L_set = C_set_1
    k = 2
    while (len(current_L_set) > 0 ):
        largeSet[k-1] = current_L_set
        current_C_set = generateCandidate(current_L_set,k)
        current_L_set = scan(transactionList=transactionList,candidateSet=current_C_set,minSupport=minSupport,freqSet=freqSet)
        k+=1

    def getSupport(item):
        """local function which Returns the support of an item"""
        # print item
        # print len(transactionList)
        return float(freqSet[item]) / len(transactionList)

    """generate assoc rules"""
    for key,value in largeSet.items()[1:]:
        for item in value:
            for subset in subsets(item):
                subset = frozenset(subset)
                remain = item.difference(subset)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(subset)
                    if confidence >=  minConf:
                        # print subset," -> ", remain
                        assocRules.append((subset,remain,confidence))
                        if confidence > getSupport(remain):
                            interestingRules.append((subset,remain))

    return largeSet,freqSet,assocRules,interestingRules

T = getTransactionList('basketData.txt')
# appearance = 50
# assocRules = list()
# while len(assocRules) == 0:
#     largeSet, freqSet, assocRules = apriori(T, appearance*1.0 / 180, 1)
#     appearance -= 1
# print appearance + 1
largeSet,freqSet,assocRules,interestingRules =  apriori(T,9.0/180,0.8)
for i in interestingRules:
    print i[0], ' -> ',i[1]
input()
for k,itemset in largeSet.items():
    print k,": ",len(itemset)
frequent_itemsets = 0
for k,itemset in largeSet.items():
    frequent_itemsets += len(itemset)
print frequent_itemsets
# print freqSet[list(largeSet[4])[0]]
for i in largeSet[4]:
    print i, " with support: ",freqSet[i]
print len(assocRules)
for i in assocRules:
    print i[0], ' -> ',i[1], ' with conf = ',i[2]
# fish_apple =0
# olive_X = 0
# for trans in T:
#     if frozenset(['Egg']).issubset(trans) and frozenset(['Nuts']).issubset(trans)and frozenset(['Ham']).issubset(trans):
#         fish_apple+=1
#         if frozenset(['Apple']).issubset(trans):
#             olive_X += 1
# print fish_apple
# print olive_X
# print [x for x in subsets(list(largeSet[4])[0])]
# print [frozenset(i) for i in list(combinations(list(largeSet[4])[0],1))]
# print getTransactionList('basketData.txt')
# print (getItemSet(T))
