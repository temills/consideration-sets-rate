#!/usr/bin/env python3
import json
from difflib import get_close_matches
import numpy as np
from analyze import *
import gensim.models.word2vec
import nltk.stem.wordnet
from itertools import combinations
import scipy
from scipy import stats

animals = get_animals()
#animals.remove("meerkat")
#animals.remove("sea lion")

#for first animal given, get the stuff that came after it
#for each first, prob of each other animal following
with open('/Users/traceymills/Documents/generation_data.csv.json') as f:
  genData = json.load(f)
numCats = 10
def generations(data):
    trialsPerCat = len(data)/numCats
    genCounts = {}
    genList = {}
    firsts = {}
    coCount = {}
    adj = {}
    after = {}
    trialLists = []
    for trial in data:
        cat = trial['category']
        if cat != 'zoo animals':    continue
        first = ''
        trialList = []
        for i in range(1, 11):
            key = 'response' + str(i)
            gen = trial[key].lower()
            matches = get_close_matches(gen, genCounts.keys(), 1, 0.85)
            if len(matches) > 0:
                gen = matches[0]
            elif gen == "bear":
                gen = "grizzly bear"
            elif gen in ["cobra", "python", "boa constrictor"]:
                gen = "snake"
            if gen in animals:
                if i==1:
                    first = gen
                    firsts[gen] = firsts.get(gen, [0, {}])
                    firsts[gen][0] = firsts[gen][0]+1
                    last = gen
                    adj[last] = adj.get(last, {})
                else:
                    firsts[first][1][gen] = firsts[first][1].get(gen, 0) + 1
                    adj[gen] = adj.get(gen, {})
                    adj[gen][last] = adj[gen].get(last, 0) + 1
                    adj[last][gen] = adj[last].get(gen, 0) + 1
            trialList.append(gen)
            genCounts[gen] = genCounts.get(gen, 0) + 1
            #genList[len(genList)-1].append(gen)
        trialLists.append(trialList)
        for a in trialList:
            coCount[a] = coCount.get(a, {})
            for a2 in trialList:
                if a2 != a:
                    coCount[a][a2] =  coCount[a].get(a2, 0) + 1
    for a in adj.keys():
        totAdj = sum([adj[a][a2] for a2 in adj[a].keys()])
        for a2 in adj[a].keys():
            adj[a][a2] = adj[a][a2]/totAdj
    return coCount, firsts, genCounts, genList, adj, trialLists
coCount, firsts, genCounts, genList, adj, trialLists = generations(genData)


#probability of generation per trial
def getGenProbs(genCounts):
    probs = {}
    tot = sum(list(genCounts.values()))/10
    for g, n in genCounts.items():
        probs[g] = n/tot
    return probs
genProbs = getGenProbs(genCounts)

#prob of other animals coming to mind when given animal comes first
def firstsProbs(firsts):
    for a in firsts.keys():
        n = firsts[a][0]
        for a2 in firsts[a][1].keys():
            firsts[a][1][a2] = (firsts[a][1][a2]/n)
    return firsts
#firsts = firstsProbs(firsts)

#print(firsts)

#prob of coocurrence for each animal (for all occurences of one animal, what percentage of time did each other animal coocccur?)
def getCoProbs(coCount, genCounts):
    coProbs = {}
    for a, aDict in coCount.items():
        coProbs[a] = {}
        n = genCounts[a]
        for a2 in aDict.keys():
            coProbs[a][a2] = (coCount[a][a2]/n)/genProbs[a2]
    return coProbs
#coProbs = getCoProbs(coCount, genCounts)
#for a in coProbs.keys():
#    print(a)
#    print(sorted(coProbs[a].items(), key=lambda item: item[1], reverse=True))

#for each animal, prob of other animal coming after it, along with prior prob of that animal
def addPriorProb():
    firsts2 = {}
    for a in firsts.keys():
        if firsts[a][0] > 0:
            firsts2[a] = firsts[a]
            #print(a + ", " + str(firsts2[a][0]))
            for a2 in firsts2[a][1].keys():
                firsts2[a][1][a2] = (firsts2[a][1][a2], genProbs[a2])
            #print(sorted(firsts2[a][1].items(), key=lambda item: item[1][0], reverse=True))
            #print("")
    return firsts2
#firsts2 = addPriorProb()

#ratings gives each animals score for each feature
data, ratings = create_dict()
#correlation between descriptors' scores for each animal and that animal's coming to mind
corrs = genDescriptorCorrelation(genProbs, ratings)

#relatedness between every animal pair, weighted by feature coming to mindness
def getRelatedness():
    resMap = {}
    m = 0
    #for each animal, make list of all other animals, and 
    for a in animals:
        resMap[a] = {}
        for a2 in animals:
            #summed difference of the two animals between ratings for each descriptor, weighted by correlation of descriptor with coming-to-mindness
            resMap[a][a2] = sum([(abs(ratings[d][a] - ratings[d][a2]) * corrs[d]) for d in ratings.keys()])
            m = max(m, resMap[a][a2])
    for a in animals:
        for a2 in animals:
            resMap[a][a2] = 1-(resMap[a][a2]/m)
    return resMap

def getRelatednessUnweighted():
    resMap = {}
    m = 0
    #for each animal, make list of all other animals, and 
    for a in animals:
        resMap[a] = {}
        for a2 in animals:
            #summed difference of the two animals between ratings for each descriptor, weighted by correlation of descriptor with coming-to-mindness
            resMap[a][a2] = sum([(abs(ratings[d][a] - ratings[d][a2])) for d in ratings.keys()])
            m = max(m, resMap[a][a2])
    for a in animals:
        for a2 in animals:
            resMap[a][a2] = 1-(resMap[a][a2]/m)
    return resMap
#rel = getRelatedness()

def coProbRelCorr(coProbs, rel):
    corrs = {}
    for a in coProbs.keys():
        x = []
        y = []
        for a2, prob in coProbs[a].items():
            pProb = genProbs[a2]
            r = rel[a][a2]
            x.append(prob/pProb)
            #x.append(prob) #ignoring prior prob
            y.append(r)
        corr = np.corrcoef(x, y)[0][1]
        corrs[a] = corr
    return corrs, sum(list(corrs.values()))/len(list(corrs.values()))
#coocCorr, ave = coProbRelCorr(coProbs, rel)

#print(coocCorr)
#print(ave)

#for a in adj.keys():
#   print(a)
#  print(sorted(adj[a].items(), key=lambda item: item[1], reverse=True))
def adjRelCorr(adj, rel):
    corrs = {}
    for a in adj.keys():
        x = []
        y = []
        for a2, prob in adj[a].items():
            pProb = genProbs[a2]
            r = rel[a][a2]
            if a == "llama":
                print(a2)
                print(r)
                print(prob)
            x.append(prob/pProb)
            #x.append(prob) #ignoring prior prob
            y.append(r)
        corr = np.corrcoef(x, y)[0][1]
        corrs[a] = corr
    return corrs, sum(list(corrs.values()))/len(list(corrs.values()))
#adjCorr, adjAve = adjRelCorr(adj, rel)
#print(adjCorr)
#print(adjAve)


def addRelatedness():
    firsts3 = {}
    for a in firsts2.keys():
        if firsts2[a][0] > 0:
            firsts3[a] = firsts2[a]
            #print(a + ", " + str(firsts3[a][0]))
            for a2 in firsts3[a][1].keys():
                x = rel[a][a2]
                firsts3[a][1][a2] = (firsts3[a][1][a2][0], firsts3[a][1][a2][1], rel[a][a2])
            #print(sorted(firsts3[a][1].items(), key=lambda item: item[1][0], reverse=True))
            #print("")
    return firsts3
#firsts3 = addRelatedness()


#how does relatedness between two animals predict probability that one animal follows the other, compared to prob of animal occuring no matter what
def relFirstsCorr():
    corrs = {}
    for a in firsts3.keys():
        x = []
        y = []
        for a2, l in firsts3[a][1].items():
            prob = l[0]
            #pProb = l[1]
            pProb = genProbs[a2]
            rel = l[2]
            x.append(prob/pProb)
            #x.append(prob) #ignoring prior prob
            y.append(rel)
        corr = np.corrcoef(x, y)[0][1]
        corrs[a] = corr
    return corrs
#corrs = relFirstsCorr()
#print(corrs)

def coProbEmbCorr(coProbs):
    # Load the model.
    model = gensim.models.word2vec.Word2Vec.load('/Users/traceymills/Codenames/word2vec.dat.5')
    # Initialize a wordnet lemmatizer for stemming.
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    corrs = {}
    for a in coProbs.keys():
        aNew = a
        if a == "polar bear" or a == "grizzly bear":
            aNew = "bear"
        x = []
        y = []
        for a2, prob in coProbs[a].items():
            a2New = a2
            if a2 == "polar bear" or a2 == "grizzly bear":
                a2New = "bear"
            pProb = genProbs[a2]
            r = model.wv.similarity(aNew, a2New)
            #x.append(prob/pProb)
            x.append(prob) #ignoring prior prob
            y.append(r)
        corr = np.corrcoef(x, y)[0][1]
        corrs[a] = corr
    return corrs, sum(list(corrs.values()))/len(list(corrs.values()))

#embCorr, embCorrAve = coProbEmbCorr(coProbs)
#print(embCorr)
#print(embCorrAve)

#find relatedness between each group of 3 successive responses, compared to relatedness of any 3 in group
#list of all in animals
#list of all those in word2vec
#both types of relatedness for all groups of 3 and 2 in animals and word2vec
#go thru every 3 in order, if come upon animal not in animals
def proximityRelatedness():
    #first word2vec
    # Load the model.
    model = gensim.models.word2vec.Word2Vec.load('/Users/traceymills/Codenames/word2vec.dat.5')
    # Initialize a wordnet lemmatizer for stemming.
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    #get all responses in word2vec vocab
    #record (average relatedness between all groups, average relatedness between consec groups) for that trial
    allRel1 = []
    allRel11 = []
    allRel12 = []
    for trial in trialLists:
        usable = []
        for a in trial:
            if a in model.wv.key_to_index:
                usable.append(a)
        #get word2vec relatedness for each group of 2, along with average
        rel1 = {}
        ave2Group = 0
        num2Group = 0
        for a in trial:
            if a not in usable: continue
            rel1[a] = {}
            for a1 in trial:
                if a1 not in usable: continue
                #if a == a1: continue
                if (rel1.get(a1, -1) != -1) and (rel1[a1].get(a, -1) != -1):
                    rel1[a][a1] = rel1[a1][a]
                else:
                    rel1[a][a1] = model.wv.similarity(a, a1)
                    num2Group = num2Group + 1
                    ave2Group = ave2Group + rel1[a][a1]
        ave2Group = ave2Group/num2Group
        #get average word relatedness for all groups of 3 in trial
        ave3Group = 0
        num3Group = 0
        for group in list(combinations(usable, 3)):
            a1 = group[0]
            a2 = group[1]
            a3 = group[2]
            groupRel = (rel1[a1][a2] + rel1[a2][a3] + rel1[a3][a1])/3
            ave3Group = ave3Group + groupRel
            num3Group = num3Group + 1
        ave3Group = ave3Group/num3Group
        #get average relatedness for all consecutive groups of 3 in trial, skip ones w unusable :(
        ave = 0
        num = 0
        for i in range(len(trial)-2):
            a1 = trial[i]
            a2 = trial[i+1]
            a3 = trial[i+2]
            if a1 not in usable or a2 not in usable or a3 not in usable:  continue
            groupRel = (rel1[a1][a2] + rel1[a2][a3] + rel1[a3][a1])/3
            ave = ave + groupRel
            num = num + 1
        ave = ave/num
        allRel1.append((ave3Group, ave))
        allRel11.append(ave3Group)
        allRel12.append(ave)
    #print(allRel1)
    print(sum(allRel11)/len(allRel11))
    print(sum(allRel12)/len(allRel12))
    
    #get all responses in animals
    #record (average relatedness between all groups, average relatedness between consec groups) for that trial
    allRel2 = []
    allRel21 = []
    allRel22 = []
    for trial in trialLists:
        usable = []
        for a in trial:
            if a in animals:
                usable.append(a)
        #get word2vec relatedness for each group of 2, along with average
        #rel2 = getRelatedness()
        rel2 = getRelatednessUnweighted()
        ave2Group = 0
        #get average word relatedness for all groups of 3 in trial
        ave3Group = 0
        num3Group = 0
        for group in list(combinations(usable, 3)):
            a1 = group[0]
            a2 = group[1]
            a3 = group[2]
            groupRel = (rel2[a1][a2] + rel2[a2][a3] + rel2[a3][a1])/3
            ave3Group = ave3Group + groupRel
            num3Group = num3Group + 1
        ave3Group = ave3Group/num3Group
        #get average relatedness for all consecutive groups of 3 in trial, skip ones w unusable :(
        ave = 0
        num = 0
        for i in range(len(trial)-2):
            a1 = trial[i]
            a2 = trial[i+1]
            a3 = trial[i+2]
            if a1 not in usable or a2 not in usable or a3 not in usable:  continue
            groupRel = (rel2[a1][a2] + rel2[a2][a3] + rel2[a3][a1])/3

            ave = ave + groupRel
            num = num + 1
        ave = ave/num
        allRel2.append((ave3Group, ave))
        allRel21.append(ave3Group)
        allRel22.append(ave)
    #print(allRel2)
    print(sum(allRel21)/len(allRel21))
    print(sum(allRel22)/len(allRel22))
  
#proximityRelatedness()

#compare consec with nonconsec groups, instead of consec with all groups
def proximityRelatedness2():
    #first word2vec
    # Load the model.
    model = gensim.models.word2vec.Word2Vec.load('/Users/traceymills/Codenames/word2vec.dat.5')
    # Initialize a wordnet lemmatizer for stemming.
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    #get all responses in word2vec vocab
    #record (average relatedness between all groups, average relatedness between consec groups) for that trial
    allRel1 = []
    allRel1nc = []
    allRel1c = []
    for trial in trialLists:
        usable = []
        for a in trial:
            if a in model.wv.key_to_index:
                usable.append(a)
        #get word2vec relatedness for each group of 2, along with average
        rel1 = {}
        ave2Group = 0
        num2Group = 0
        for a in trial:
            if a not in usable: continue
            rel1[a] = {}
            for a1 in trial:
                if a1 not in usable: continue
                #if a == a1: continue
                if (rel1.get(a1, -1) != -1) and (rel1[a1].get(a, -1) != -1):
                    rel1[a][a1] = rel1[a1][a]
                else:
                    rel1[a][a1] = model.wv.similarity(a, a1)
                    num2Group = num2Group + 1
                    ave2Group = ave2Group + rel1[a][a1]
        ave2Group = ave2Group/num2Group
        
        #get average relatedness for all consecutive groups of 3 in trial, skip ones w unusable :(
        ave = 0
        num = 0
        consec1 = []
        #cRels1 = []
        for i in range(len(trial)-2):
            a1 = trial[i]
            a2 = trial[i+1]
            a3 = trial[i+2]
            if a1 not in usable or a2 not in usable or a3 not in usable:  continue
            consec1.append([a1, a2, a3])
            groupRel = (rel1[a1][a2] + rel1[a2][a3] + rel1[a3][a1])/3
            #cRels1.append(groupRel)
            ave = ave + groupRel
            num = num + 1
        ave = ave/num
        #get average word relatedness for all nonconsecutive groups of 3 in trial 
        ave3Group = 0
        num3Group = 0
        #ncRels1 = []
        for group in list(combinations(usable, 3)):
            a1 = group[0]
            a2 = group[1]
            a3 = group[2]
            #only want nonconsec groups
            if [a1, a2, a3] in consec1 or [a1, a3, a2] in consec1 or [a2, a1, a3] in consec1 or [a2, a3, a1] in consec1 or [a3, a2, a1] in consec1 or [a3, a1, a2] in consec1: continue
            groupRel = (rel1[a1][a2] + rel1[a2][a3] + rel1[a3][a1])/3
            #ncRels1.append(groupRel)
            ave3Group = ave3Group + groupRel
            num3Group = num3Group + 1
        ave3Group = ave3Group/num3Group
        allRel1.append((ave3Group, ave))
        allRel1nc.append(ave3Group)
        allRel1c.append(ave)
    
    print(allRel1)
    scipy.stats.ttest_rel(allRel1c, allRel1nc)
    print("")
    print("Word embedding similarity")
    print("--------------------------")
    print("Average nonconsecutive similarity: " + str(sum(allRel1nc)/len(allRel1nc)))
    print("Average consecutive similarity: " + str(sum(allRel1c)/len(allRel1c)))
    print("t-score and p-value: " + str(scipy.stats.ttest_rel(allRel1c, allRel1nc)))
    

    #get all responses in animals
    #record (average relatedness between all groups, average relatedness between consec groups) for that trial
    allRel2 = []
    allRel2nc = []
    allRel2c = []
    for trial in trialLists:
        #trial = trial[3:len(trial)]
        usable = []
        for a in trial:
            if a in animals:
                usable.append(a)
        #get word2vec relatedness for each group of 2, along with average
        #rel2 = getRelatedness()
        rel2 = getRelatednessUnweighted()
        ave2Group = 0
        #get average relatedness for all consecutive groups of 3 in trial, skip ones w unusable :(
        consec2 = []
        ave = 0
        num = 0
        for i in range(len(trial)-2):
            a1 = trial[i]
            a2 = trial[i+1]
            a3 = trial[i+2]
            if a1 not in usable or a2 not in usable or a3 not in usable:  continue
            consec2.append([a1, a2, a3])
            groupRel = (rel2[a1][a2] + rel2[a2][a3] + rel2[a3][a1])/3
            #cRels2.append(groupRel)
            ave = ave + groupRel
            num = num + 1
        if num == 0:
            continue
        ave = ave/num
        #get average word relatedness for all groups of 3 in trial
        ave3Group = 0
        num3Group = 0
        for group in list(combinations(usable, 3)):
            a1 = group[0]
            a2 = group[1]
            a3 = group[2]
            #only want nonconsec groups
            if [a1, a2, a3] in consec2 or [a1, a3, a2] in consec2 or [a2, a1, a3] in consec2 or [a2, a3, a1] in consec2 or [a3, a2, a1] in consec2 or [a3, a1, a2] in consec2: continue
            groupRel = (rel2[a1][a2] + rel2[a2][a3] + rel2[a3][a1])/3
            ave3Group = ave3Group + groupRel
            num3Group = num3Group + 1
        ave3Group = ave3Group/num3Group
        allRel2.append((ave3Group, ave))
        allRel2nc.append(ave3Group)
        allRel2c.append(ave)
    print(allRel2)
    print("")
    print("Feature based similarity")
    print("--------------------------")
    print("Average nonconsecutive similarity: " + str(sum(allRel2nc)/len(allRel2nc)))
    print("Average consecutive similarity: " + str(sum(allRel2c)/len(allRel2c)))
    print("t-score and p-value: " + str(scipy.stats.ttest_rel(allRel2c, allRel2nc)))

proximityRelatedness2()