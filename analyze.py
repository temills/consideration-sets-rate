#!/usr/bin/env python3

#64 animals
#8 animals per participant
#want at least 5 datapoints per animal?
#about 8*5 = 40

import json
from difflib import get_close_matches
import numpy as np
import random
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
import pandas as pd
from factor_analyzer.factor_analyzer import calculate_kmo


####################################
#first used "large", "cute", "cool", "normal", "striking", "dangerous", "desert", "forest", "tropics", "water", "land", "arctic", "lifespan", "think", "awake", "diet", "type"]
#then "has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"
#did first speed analysis with "has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little" and "large", "cool", "striking", "dangerous", "lifespan"
#second speed analysis with "cute", "normal", "desert", "forest", "tropics", "water", "land", "arctic", "lifespan", "think", "awake", "diet", "type"
#rating data
#with open('/Users/traceymills/consideration/consideration-sets-rate/rate_data.csv.json') as f1:
#  animals_1 = json.load(f1)
#with open('/Users/traceymills/consideration/consideration-sets-rate/rate_data2.csv.json') as f2:
#  animals_2 = json.load(f2)
#with open('/Users/traceymills/consideration/consideration-sets-rate/vegetables.json') as f3:
#  vegetables = json.load(f3)
with open('/Users/traceymills/consideration/consideration-sets-rate/restaurants.json') as f4:
  restaurants = json.load(f4)
resDescriptors = ["think", "likes", "popular", "many locations", "is unique", "healthy", "brightly colored logo", "lively", "variety", "well decorated", "expensive", "quick", "casual"]
#resDescriptors = ["interesting side dishes", "soft food", "cold food", "desserts"]
restaurantList = [str.lower(res) for res in ['Mcdonalds', 'Burger King', 'Wendys', 'Taco Bell', 'Applebees', 'Chilis', 'Olive Garden', 'Arbys', 'Pizza Hut', 'Chipotle', 'TGI Fridays', 'Subway', 'Red Lobster', 'Chick Fil A', 'Kentucky Fried Chicken', 'Outback Steakhouse', 'Red Robin', 'Dennys', 'Cheesecake Factory', 'Panera', 'Buffalo Wild Wings', 'Popeyes', 'Dominos', 'IHOP', 'Dairy Queen', 'Five Guys', 'Hardees', 'Panda Express', 'Starbucks', 'Cracker Barrel', 'Jimmy Johns', 'Sonic', 'Jack in the Box', 'Ruby Tuesdays', 'PF Changs', 'Hooters', 'Papa Johns', 'Texas Roadhouse', 'Little Ceasars', 'Dunkin Donuts', 'Long John Silvers', 'Maggianos']];


with open('/Users/traceymills/consideration/consideration-sets-rate/vegetables.json') as f5:
  vegetables = json.load(f5)
vegDescriptors = ["colorful", "think", "dishes", "popular", "likes", "available", "healthy", "fragrant", "warm", "sweet", "large", "crunchy", "heavy", "calories"]
vegetableList = ['carrots', 'broccoli', 'lettuce', 'peas', 'potatoes', 'onions', 'cauliflower', 'corn', 'green beans', 'tomatoes', 'cucumbers', 'spinach', 'squash', 'celery', 'peppers', 'eggplant', 'cabbage', 'asparagus', 'brussel sprouts', 'kale', 'turnips', 'zucchini', 'garlic', 'pumpkins', 'beets', 'mushrooms', 'radish', 'okra', 'yams', 'sweet potatoes', 'arugula', 'sprouts', 'artichoke', 'parsnips', 'bok choy', 'lima beans', 'avocado', 'snap peas', 'leeks', 'collard greens']


descriptors1 = ["large", "cool", "striking", "dangerous", "lifespan"]
descriptors2 = ["has large feet relative to its body size", "quiet", "has good hearing", "has long hair", "sleeps very little"]
#questions = []
#questions2 = []


with open('/Users/traceymills/consideration/consideration-sets-rate/rate_data.csv.json') as f5:
  animals = json.load(f5)
descriptors = ["large", "cute", "cool", "normal", "striking", "dangerous"]
questions = ["desert", "forest", "tropics", "water", "land", "arctic", "lifespan", "think", "awake"]
questions2 = ["type", "diet"]
animalList = ["leopard", "chimp", "beetle", "llama", "hyena", "mouse", "horse", "goat", "zebra", "antelope", "sea lion", "fox", "deer", "tarantula", "bat", "meerkat", "buffalo", "giraffe", "bull", "whale", "rabbit", "lion", "hippo", "baboon", "bird", "monkey", "snake", "tiger", "panther", "kangaroo", "owl", "elephant", "otter", "rhino", "cheetah", "gazelle", "alligator", "penguin", "panda", "parrot", "eagle", "polar bear", "koala", "ostrich", "crocodile", "dolphin", "lemur", "turtle", "gorilla", "wolf", "shark", "cow", "peacock", "jaguar", "camel", "platypus", "flamingo", "duck", "sloth", "seal", "grizzly bear", "lizard", "fish"]
#animals = ["leopard", "chimp", "beetle", "llama", "hyena", "mouse", "horse", "goat", "zebra", "antelope", "sea lion", "fox", "deer", "tarantula", "bat", "meerkat", "buffalo", "bull", "whale", "rabbit", "hippo", "baboon", "bird", "monkey", "snake", "panther", "kangaroo", "owl", "otter", "cheetah", "gazelle", "penguin", "panda", "parrot", "eagle", "polar bear", "koala", "ostrich", "crocodile", "dolphin", "lemur", "turtle", "gorilla", "wolf", "shark", "cow", "peacock", "jaguar", "camel", "platypus", "flamingo", "duck", "sloth", "seal", "grizzly bear", "lizard", "fish"]
#removed giraffe, lion, tiger, elephant, rhino, alligator
#animals = ["leopard", "chimp", "beetle", "llama", "hyena", "mouse", "horse", "goat", "antelope", "sea lion", "fox", "deer", "tarantula", "bat", "meerkat", "buffalo", "bull", "whale", "rabbit", "hippo", "baboon", "bird", "snake", "panther", "kangaroo", "owl", "otter", "rhino", "cheetah", "gazelle", "alligator", "penguin", "panda", "parrot", "eagle", "polar bear", "koala", "ostrich", "crocodile", "dolphin", "lemur", "turtle", "gorilla", "wolf", "shark", "cow", "peacock", "jaguar", "camel", "platypus", "flamingo", "duck", "sloth", "seal", "lizard", "fish"]
#removed zebra, lion, giraffe, elephant, tiger, grizzly bear, monkey
descriptors = ["think"]

with open('/Users/traceymills/consideration/consideration-sets-rate/sports.json') as f6:
  sports = json.load(f6)
sportList = ['baseball', 'football', 'soccer', 'tennis', 'hockey', 'basketball', 'running', 'golf', 'volleyball', 'swimming', 'cricket', 'lacrosse', 'boxing', 'rugby', 'gymnastics', 'wrestling', 'ice skating', 'softball', 'bowling', 'skiing', 'polo', 'badminton', 'racecar driving', 'horseback riding', 'fencing', 'cheerleading', 'ping pong', 'biking', 'squash', 'curling', 'diving', 'raquetball', 'field hockey', 'water polo', 'handball', 'dance', 'snowboarding']
descriptors = ['think', 'likes', 'popular', 'high energy', 'dangerous', 'strenuous', 'spectators', 'competitive', 'agility', 'expensive', 'space', 'been around', 'learn', 'flexibility']

with open('/Users/traceymills/consideration/consideration-sets-rate/holidays.json') as f7:
  holidays = json.load(f7)
holidayList = ['Christmas', 'Thanksgiving', 'Fourth of July', 'Easter', 'Labor Day', 'Memorial Day', 'New Years', 'Halloween', 'Valentines Day', 'Veterans Day', 'Martin Luther King Jr. Day', 'Presidents Day', "St. Patricks Day", 'Hanukkah', 'Kwanza', 'Mothers Day', 'Fathers Day', 'Christopher Columbus Day', 'Passover', 'Birthdays', 'Chinese New Year', 'Ramadan', 'Cinco de Mayo', 'Earth Day', 'Flag Day', 'Diwali', 'Juneteenth', 'Winter Solstice', 'Boxing Day']
descriptors = ['religious', 'political', 'around', 'family oriented', 'partying', 'time off', 'romantic', 'traditions', 'food', 'likes', 'think', 'widely celebrated', 'reflective', 'joyous', 'meaningful', 'early']


def get_animals():
    return animals

def create_dict(trial_data, an):
    data = {}
    for trial in trial_data:
        a = trial["animal"]
        if a not in animals:
            continue
        for d in descriptors:
            if d in trial.keys():
                if an == True:
                    if trial[q] == "very rarely": n=0
                    if trial[q] == "rarely": n=1
                    if trial[q] == "an average amount": n=2
                    if trial[q] == "often": n=3
                    if trial[q] == "very often": n=4
                    data[d] = data.get(d, {})   #dict for descriptor d
                    data[d][a] = data[d].get(a, [[], 0, 0])   #list of responses, num responses, average
                    data[d][a][0].append(n)
                    data[d][a][1] = data[d][a][1] + 1
                else:
                    data[d] = data.get(d, {})   #dict for descriptor d
                    data[d][a] = data[d].get(a, [[], 0, 0])   #list of responses, num responses, average
                    data[d][a][0].append(int(trial[d]))
                    data[d][a][1] = data[d][a][1] + 1
    data2 = {}
    for d, d_dict in data.items():
        data2[d] = {}
        for a in d_dict.keys():
            if data[d][a][1] == 0:
                data[d][a][2] = 0
            else:
                data[d][a][2] = sum(data[d][a][0])/data[d][a][1]
            data2[d][a] = data[d][a][2]    
    for a in animals:
        for d in data2.keys():
            data2[d][a] = data2[d].get(a, 0)

    return data, data2

def create_dict2(trial_data, descriptors, x):
    data = {}
    allItems = []
    for trial in trial_data:
        a = str.lower(trial[x])
        allItems.append(a)
        for d in descriptors:
            data[d] = data.get(d, {})   #dict for descriptor d
            data[d][a] = data[d].get(a, [[], 0, 0])   #list of responses, num responses, average
            if x == "animal":
                if trial[d] == "very rarely": n=0
                if trial[d] == "rarely": n=1
                if trial[d] == "an average amount": n=2
                if trial[d] == "often": n=3
                if trial[d] == "very often": n=4
                data[d][a][0].append(n)
            else:
                data[d][a][0].append(int(trial[d]))
            data[d][a][1] = data[d][a][1] + 1
    data2 = {}
    for d, d_dict in data.items():
        data2[d] = {}
        for a in d_dict.keys():
            if data[d][a][1] == 0:
                data[d][a][2] = 0
            else:
                data[d][a][2] = sum(data[d][a][0])/data[d][a][1]
            data2[d][a] = data[d][a][2]
    
    for a in allItems:
        for d in data2.keys():
            data2[d][a] = data2[d].get(a, 0)

    return data, data2

data, ratings = create_dict2(holidays, descriptors, "item")

def num_res_per_a(data):
    nums = []
    for a in animals:
        nums.append(len(data["large"][a][0]))
#num_res_per_a(data)


################################
#generation data
with open('/Users/traceymills/Documents/generation_data.csv.json') as f:
  gen_data = json.load(f)
def generations(category, items):
    data = gen_data
    numCats = 10
    trialsPerCat = len(data)/numCats
    #print(trialsPerCat)
    genCounts = {}
    genList = {}
    #animalsTemp = ["leopard", "chimp", "beetle", "llama", "hyena", "mouse", "horse", "goat", "zebra", "antelope", "sea lion", "fox", "deer", "tarantula", "bat", "meerkat", "buffalo", "giraffe", "bull", "whale", "rabbit", "lion", "hippo", "baboon", "bird", "monkey", "snake", "tiger", "panther", "kangaroo", "owl", "elephant", "otter", "rhino", "cheetah", "gazelle", "alligator", "penguin", "panda", "parrot", "eagle", "polar bear", "koala", "ostrich", "crocodile", "dolphin", "lemur", "turtle", "gorilla", "wolf", "shark", "cow", "peacock", "jaguar", "camel", "platypus", "flamingo", "duck", "sloth", "seal", "grizzly bear", "lizard", "fish"]
    for trial in data:
        cat = trial['category']
        genCounts[cat] = genCounts.get(cat, {})
        genList[cat] = genList.get(cat, [])
        genList[cat].append([])
        for i in range(1, 11):
            key = 'response' + str(i)
            gen = trial[key].lower()
            if len(get_close_matches(gen, ["n/a", "na", "dont know", "none"], 1, 0.85)) > 0:
                continue
            #animalsTemp.append(list(genCounts[cat].keys()))
            matches = get_close_matches(gen, items, 1, 0.85)
            if len(matches) > 0:
                gen = matches[0]
            elif gen == "bear":
                gen = "grizzly bear"
            #else:
                #print(gen)            #still add generated animals in if they weren't asked about...?
            genCounts[cat][gen] = genCounts[cat].get(gen, 0) + 1
            genList[cat][len(genList[cat])-1].append(gen)
        genList[cat][len(genList[cat])-1] = list(set(genList[cat][len(genList[cat])-1]))
    return genCounts[category], genList[category]
genCounts, x = generations('holidays', "item")


def getGenProbs(genCounts):
    probs = {}
    tot = sum(list(genCounts.values()))
    for g, n in genCounts.items():
        probs[g] = n/tot
    return probs
probs = getGenProbs(genCounts)

#print(genCounts)
#print(sorted(probs.items(), key=lambda item: item[1], reverse=True))



#####################################
#combine data
#print(ratings)
#correlations between animals score for descriptors and animals prob. of coming to mind
def genDescriptorCorrelation(probs, ratings):
    correlations = {}
    for d, d_dict in ratings.items():
        x, y = [], []
        for a, n in d_dict.items():
            x.append(n) #average rating for item
            y.append(probs.get(a, 0)) #probability of generation for item
        correlations[d] = np.corrcoef(x, y)[0][1]
    return correlations
corrs = genDescriptorCorrelation(probs, ratings)
print(corrs)

#get think data
#print("restaurants:")
genCounts, genList = generations('chain restaurants', restaurantList)
data, ratings = create_dict2(restaurants, ["think"], "item")
probs = getGenProbs(genCounts)
corrs = genDescriptorCorrelation(probs, ratings)
#print(corrs)

#print("vegetables:")
genCounts, genList = generations('vegetables', vegetableList)
data, ratings = create_dict2(vegetables, ["think"], "item")
probs = getGenProbs(genCounts)
corrs = genDescriptorCorrelation(probs, ratings)
#print(corrs)

#print("animals:")
genCounts, genList = generations('zoo animals', animalList)
data, ratings = create_dict2(animals, ["think"], "animal")
probs = getGenProbs(genCounts)
corrs = genDescriptorCorrelation(probs, ratings)
#print(corrs)



#print("Ratings for Descriptors:")
def topDescriptors():
    striking = []
    dangerous = []
    lifespan = []
    large = []
    for a in animals:
        striking.append(ratings["striking"][a])
        dangerous.append(ratings["dangerous"][a])
        lifespan.append(ratings["lifespan"][a])
        large.append(ratings["large"][a])
    print("striking:")
    print(striking)
    print("dangerous:")
    print(dangerous)
    print("lifespan:")
    print(lifespan)
    print("large:")
    print(large)
#topDescriptors()



######################################
#factor analysis
#want columns are descriptors, rows are animals, values are average scores
def isFactorable(ratings):
    cols = list(ratings.keys())
    dfl = []
    for i in range(len(animals)):
        l = []
        #for j in range(len(cols)):
        #    l.append(ratings[cols[j]][animals[i]])
        #dfl.append(l)
        dfl.append([ratings[cols[j]][animals[i]] for j in range(len(cols))])
    df = pd.DataFrame(dfl, columns=cols)
    df.dropna(inplace=True)
    chi_square_value,p_value=calculate_bartlett_sphericity(df)
    kmo_all,kmo_model=calculate_kmo(df)
    return df,chi_square_value,p_value, kmo_all, kmo_model

#df, chi_square_value, p_value, kmo_all, kmo_model = isFactorable(ratings)
#print(chi_square_value, p_value)
#print(kmo_all, kmo_model)

def getNumFactors(df):
    fa = FactorAnalyzer()
    fa.fit(df)
    # Check Eigenvalues
    ev, v = fa.get_eigenvalues()
    return(ev, v)

#ev, v = getNumFactors(df)
#print(ev)   #gives 11 more than 1
#print(v)

def factor(df, n):
    fa = FactorAnalyzer(rotation="varimax", n_factors=n)
    fa.fit(df)
    return fa.loadings_, df.columns
#arrs, cols = factor(df, 6)

def colsInFactor(arrs, cols):
    factors = {}
    for i in range(len(arrs[0])):
        factors[i] = {}
        for j in range(len(cols)):
            if abs(arrs[j][i]) >= 0.5:
                factors[i][cols[j]] = arrs[j][i]
    return factors
#factors = colsInFactor(arrs, cols)
#print("Factors:")
#print(factors)

####################
#how to get correlation between factors and coming to mind?
#each animal has certain score for each descriptor
#each descriptor has correlation with factor
#can plot animals in factor space - for one factor, animals point is average of animals correlation with descriptor*loading for that factor for each descriptor?
#see correlation of factor with coming to mind by looking at each animals score for that factor, correlation with coming to mind

#animals relatedness to each factor
def scoreAnimalsPerFactor(factors):
    numFactors = len(list(factors.keys()))
    animalFactorScores = {}
    for i in range(numFactors): #iterate through factors, saving animal score list for each
        scoreList = []
        dDict = factors[i]      #descriptor loadings for this factor
        for j in range(len(animals)):   #iterate through all the animals
            a = animals[j]
            sum = 0
            for d, loading in dDict.items():
                sum = sum + (ratings[d][a]*loading)     #sum rating of animal for each descriptor, weighted by desriptor loading for given factor
            scoreList.append(sum/len(list(dDict.items())))     #record scores in same order as animals
        animalFactorScores[i] = scoreList
    return animalFactorScores

#animalFactorScores = scoreAnimalsPerFactor(factors)
#print("Animal factor scores:")
#print(animalFactorScores)
#get correlation between each factor and probability of coming to mind
def genFactorCorrelation(probs, animalFactorScores):
    correlations = {}
    for f, aScores in animalFactorScores.items():
        x, y = [], []
        for i in range(len(animals)):
            x.append(aScores[i]) #average score for animal for this factor
            y.append(probs.get(animals[i], 0)) #probability of generation for animal
        correlations[f] = np.corrcoef(x, y)[0][1]
    return correlations
#corrs = genFactorCorrelation(probs, animalFactorScores)
#print(corrs)

#now plot animals along factor space, colored with probability of coming to mind
def animalsData(probs, animalFactorScores):
    xdata = animalFactorScores[0] #animal scores w first factor
    ydata = animalFactorScores[1] #animal scores w second factor
    zdata = animalFactorScores[2] #animal scores w third factor
    data = [xdata, ydata, zdata]
    colors = []
    for a in animals:
        #if probs.get(a, 0) == 0:
            #print(a + ": " + str(probs.get(a, 0)))
        colors.append(probs.get(a, 0))
    return data, colors

#data, colors = animalsData(probs, animalFactorScores)
#print("colors:")
#print(colors)

#print(sorted(ratings["striking"].items(), key=lambda item: item[1], reverse=True)[0:10])
#print(sorted(ratings["large"].items(), key=lambda item: item[1], reverse=True)[0:10])
#print(sorted(ratings["dangerous"].items(), key=lambda item: item[1], reverse=True)[0:10])

# for q in questions2:
#             data[q] = data.get(q, {})
#             data[q][a] = data[q].get(a, {})
#             data[q][a][trial[q]] = data[q][a].get(trial[q], 0) + 1
#         for q in questions:
#             data[q] = data.get(q, {})   #dict for descriptor d
#             data[q][a] = data[q].get(a, [[], 0, 0])   #list of responses, num responses, average
#             n = 0
#             if q == "lifespan":
#                 if trial[q] == "short": n=0
#                 if trial[q] == "medium": n=1
#                 if trial[q] == "long": n=2
#             if q == "think":
#                 if trial[q] == "very rarely": n=0
#                 if trial[q] == "rarely": n=1
#                 if trial[q] == "an average amount": n=2
#                 if trial[q] == "often": n=3
#                 if trial[q] == "very often": n=4
#             if q == "awake":
#                 if trial[q] == "day": n=1
#                 else: n=0
#             else:
#                 if trial[q] == "yes": n=1
#                 if trial[q] == "no": n=0
#                 if trial[q] == "dont know": n == 0.5
#             data[q][a][0].append(n)
#             data[q][a][1] = data[q][a][1] + 1


        
