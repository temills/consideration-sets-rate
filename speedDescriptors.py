#!/usr/bin/env python3

import json
from difflib import get_close_matches
import numpy as np
import random
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
import pandas as pd
from factor_analyzer.factor_analyzer import calculate_kmo

#get correlation between descriptors and coming to mind, for high and low relevance descriptors
####################################
#rating data
with open('/Users/traceymills/consideration/consideration-sets-rate/rate_data.csv.json') as f1:
  trial_data1 = json.load(f1)
with open('/Users/traceymills/consideration/consideration-sets-rate/rate_data2.csv.json') as f2:
  trial_data2 = json.load(f2)
descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan"]
descriptors2 = ["has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"]
animals = ["leopard", "chimp", "beetle", "llama", "hyena", "mouse", "horse", "goat", "zebra", "antelope", "sea lion", "fox", "deer", "tarantula", "bat", "meerkat", "buffalo", "giraffe", "bull", "whale", "rabbit", "lion", "hippo", "baboon", "bird", "monkey", "snake", "tiger", "panther", "kangaroo", "owl", "elephant", "otter", "rhino", "cheetah", "gazelle", "alligator", "penguin", "panda", "parrot", "eagle", "polar bear", "koala", "ostrich", "crocodile", "dolphin", "lemur", "turtle", "gorilla", "wolf", "shark", "cow", "peacock", "jaguar", "camel", "platypus", "flamingo", "duck", "sloth", "seal", "grizzly bear", "lizard", "fish"]

def get_animals():
    return animals

def create_dict():
    data = {}
    #get animal descriptor rating data from all trials
    for trial_data in [trial_data1, trial_data2]:
        for trial in trial_data:
            a = trial["animal"]
            if a not in animals:
                continue
            if trial_data == trial_data1:   descriptors = descriptors1
            else:   descriptors = descriptors2
            for d in descriptors:
                data[d] = data.get(d, {})   #dict for descriptor d
                data[d][a] = data[d].get(a, [[], 0, 0])   #list of responses, num responses, average     
                n = 0
                if d == "lifespan":
                    if trial[d] == "short": n=0
                    if trial[d] == "medium": n=1
                    if trial[d] == "long": n=2
                else:
                    n = int(trial[d])
                data[d][a][0].append(n)
                data[d][a][1] = data[d][a][1] + 1
    data2 = {}
    #get just average ratings from more detailed data
    for d, d_dict in data.items():
        data2[d] = data2.get(d, {})
        for a in d_dict.keys():
            #if num responses 0 for this animal/descriptor pair :/ (all g rn)
            #if data[d][a][1] == 0:
            #    data[d][a][2] = 0 #make average 0
            #else:
            #    data[d][a][2] = sum(data[d][a][0])/data[d][a][1] #calc average
            cata[d][a][2] = sum(data[d][a][0])/data[d][a][1] #calc average
            data2[d][a] = data[d][a][2]
    
    #check that has rating for each animal for each descriptor (all g rn)
    #for a in animals:
    #    for d in data2.keys():
    #        if data2[d].get(a, -1) == -1:
    #            print("uh oh - " + d + ", " + a)
    #            data2[d][a] = data2[d].get(a, 0)

    return data2
ratings = create_dict()

################################
#generation data
with open('/Users/traceymills/Documents/generation_data.csv.json') as f:
  gen_data = json.load(f)
def generations():
    data = gen_data
    numCats = 10
    trialsPerCat = len(data)/numCats
    genCounts = {}
    genList = {}
    for trial in data:
        cat = trial['category']
        if cat != "zoo animals":
            continue
        genCounts[cat] = genCounts.get(cat, {})
        genList[cat] = genList.get(cat, [])
        genList[cat].append([])
        for i in range(1, 11):
            key = 'response' + str(i)
            gen = trial[key].lower()
            if len(get_close_matches(gen, ["n/a", "na", "dont know", "none"], 1, 0.85)) > 0:
                continue
            #animalsTemp.append(list(genCounts[cat].keys()))
            matches = get_close_matches(gen, animals, 1, 0.85)
            if len(matches) > 0:
                gen = matches[0]
            elif gen == "bear":
                gen = "grizzly bear"
            #else:
                #print(gen)            #still add generated animals in if they weren't asked about...?
            genCounts[cat][gen] = genCounts[cat].get(gen, 0) + 1
            genList[cat][len(genList[cat])-1].append(gen)
        genList[cat][len(genList[cat])-1] = list(set(genList[cat][len(genList[cat])-1]))
    return genCounts["zoo animals"], genList["zoo animals"]
genCounts, genList = generations()

def getGenProbs(genCounts):
    probs = {}
    tot = sum(list(genCounts.values()))
    for g, n in genCounts.items():
        probs[g] = n/tot
    return probs
probs = getGenProbs(genCounts)

#correlations between animals score for descriptors and animals prob. of coming to mind
def genDescriptorCorrelation(probs, ratings):
    correlations = {}
    for d, d_dict in ratings.items():
        x, y = [], []
        for a, n in d_dict.items():
            x.append(n) #average rating for animal
            y.append(probs.get(a, 0)) #probability of generation for animal
        correlations[d] = np.corrcoef(x, y)[0][1]
    return correlations
corrs = genDescriptorCorrelation(probs, ratings)
print(corrs)