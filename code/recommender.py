"""
CSCI-B659: SP22 Final Project, Ethan Eldridge

The following code is an adapted content-based recommender system based on the work of Balog et al. The paper
can be found at the following link: https://research.google/pubs/pub48182/

Before running the code, simply add your candidate (item) database to the item variable as a comma-separated list of strings. 
The program will then walk you through the rating and tagging process. Be SURE that the tags you enter are EXACTLY the same if 
you intend for them to be (i.e. if you want to tag two candidates as "tall", make sure one of them isn't tagged as " tall" or "Tall).

If you don't want to add your own items and simply want to repeat the experimental results from the associated paper, comment out 
everything below the "import math" line and above the "#TODO: Uncomment for experimental results" line, then uncomment the section 
below the TODO.

"""
import numpy as np 
from scipy.stats import wilcoxon
import sys

NEUTRAL = 0
K = 15
# TODO:
MU = 1
import math

items = []
seen = [0 for i in items]
# Dict holding ratings for each item
itemRatings = {}
# Dict holding tags for each item (tags[item]=[tags,])
tags = {}
# Creating tag and rating dicts
for i in items:
    tags[str(i)] = []
    itemRatings[str(i)] = 0

cont = 1
# While the user wants to rate/tag:
while cont:
    if not (0 in seen):
        print("No items to rate or tag... :(")
        cont = 0
        break
    # Displaying items to the user
    print("*"*38)
    print("** Items available to Rate and Tag: **")
    print("*"*38)   
    for i in range(len(items)):
        if seen[i] == 1:
            continue
        else:
            print(str(i) + ": " + str(items[i]))
    print()
    # Ask which items the user would like to rate/tag
    print("Which of the above items would you like to rate and tag?")
    while(True):
        try:
            ind = input("Please enter the number of the item here: ")
            if (int(ind) not in range(len(items))):
                raise ValueError
            else:
                ind = int(ind)
                print("\n\n")
                break
        except ValueError:
            print("Invalid input.")
    chosen = str(items[ind])
    seen[ind] = 1
    # Rate item
    while(True):
        try:
            rating = input("Please rate " + chosen + " on a scale of 0-10: ")
            if (float(rating) not in range(0,11)):
                raise ValueError
            else:
                rating = float(rating)
                # Normalize rating on scale of [-1,1] instead of [0,10]
                itemRatings[chosen] = 0.2*rating-1
                print("\n\n")
                break
        except ValueError:
            print("Invalid input.")
    # Tag item
    print("Please tag " + chosen + " with any relevant words or phrases.")
    print("Type the tag and hit Enter to add it. Type 'exit' and hit Enter to submit your tags:\n")  
    last = ""
    while last != "exit":
        last = input("")
        if last == "exit": break
        if last == "":
            while last=="":
                print("Invalid input. Please try again.")
                last = input("")
            if last == "exit": break
        tags[chosen].append(last)
    print("\n\n")
    # Prompt to keep ranking/tagging or move on
    print("Summary:")
    print("You gave " + chosen + " the following rating: " + str(rating) + "/10.")
    print("You also gave " + chosen + " the following tags: ")
    for t in tags[chosen]:
        print("· " + t)
    print()
    ("Would you like to continue rating?")
    while(True):
        try:
            cont = input("Enter 0 to stop, or 1 to continue: ")
            if (int(cont) != 0) and (int(cont) !=1):
                raise ValueError
            else:
                cont = int(cont)
                print("\n\n")
                break
        except ValueError:
            print("Invalid input.")


#TODO: Uncomment for experimental results
# items = ["Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Charlotte", "William", "Sophia", "James", "Amelia", "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Evelyn", "Alexander", "Harper", "John", "Mary Katherine", "David", "Kayla", "Nathan", "Stella", "Maximilian", "Lilly", "Mohamed", "Maria"]
# seen = [1 for i in range(len(items))]
# itemRatings = {'Liam': 0.9480470476872822, 'Olivia': 0.2800225838472101, 'Noah': -0.2394419242859699, 'Emma': 0.23293072267229004, 'Oliver': 0.47087383108787556, 'Ava': -0.4384836767786818, 'Elijah': 0.24843598284334817, 'Charlotte': -0.16030628543893627, 'William': 0.4096848762842971, 'Sophia': 0.9321975188999886, 'James': 0.3480911521686434, 'Amelia': -0.1255552743051973, 'Benjamin': -0.11753656780286381, 'Isabella': 0.31981428718018556, 'Lucas': 0.6373402056875143, 'Mia': -0.08700279272318229, 'Henry': 0.7953361351773416, 'Evelyn': 0.8761852027939598, 'Alexander': 0.8550660293960118, 'Harper': 0.9121927046502898, 'John': -0.09578711984289917, 'Mary Katherine': -0.3798055336849258, 'David': 0.2772122237281829, 'Kayla': -0.36776225910671356, 'Nathan': -0.3222163345693743, 'Stella': 0.7826065129785811, 'Maximilian': 0.6098449528401374, 'Lilly': 0.20157858997777311, 'Mohamed': 0.8471909689937163, 'Maria': 0.2742612838773275}
# tags = {'Liam': ['Good GPA', 'Grad degree', 'Little work experience', 'Volunteer'], 'Olivia': ['Good GPA', 'Purdue grad', 'From Indiana'], 'Noah': ['Bad GPA', 'Little work experience'], 'Emma': ['Good GPA', 'Purdue grad', 'From Indiana'], 'Oliver': ['Good GPA', 'Purdue grad', 'From Indiana', 'Little work experience', 'Volunteer'], 'Ava': ['Bad GPA', 'Little work experience'], 'Elijah': ['Good GPA', 'Purdue grad', 'From Indiana', 'Little work experience', 'Volunteer'], 'Charlotte': ['Bad GPA', 'Little work experience'], 'William': ['Good GPA', 'Purdue grad', 'From Indiana', 'Little work experience', 'Volunteer'], 'Sophia': ['Good GPA', 'Grad degree', 'Little work experience', 'Volunteer'], 'James': ['Good GPA', 'Purdue grad', 'From Indiana'], 'Amelia': ['Bad GPA', 'Little work experience'], 'Benjamin': ['Bad GPA', 'Little work experience'], 'Isabella': ['Good GPA', 'Purdue grad', 'From Indiana'], 'Lucas': ['Good GPA', 'Grad degree', 'From Indiana'], 'Mia': ['Bad GPA', 'Little work experience'], 'Henry': ['Good GPA', 'Grad degree', 'From Indiana'], 'Evelyn': ['Good GPA', 'Grad degree', 'Little work experience', 'Volunteer'], 'Alexander': ['Good GPA', 'Grad degree', 'From Indiana'], 'Harper': ['Good GPA', 'Grad degree', 'Little work experience', 'Volunteer'], 'John': ['Bad GPA', 'Little work experience'], 'Mary Katherine': ['Bad GPA', 'Little work experience'], 'David': ['Good GPA', 'Purdue grad', 'From Indiana'], 'Kayla': ['Bad GPA', 'Little work experience'], 'Nathan': ['Bad GPA', 'Little work experience'], 'Stella': ['Good GPA', 'Grad degree', 'Little work experience', 'Volunteer'], 'Maximilian': ['Good GPA', 'Grad degree', 'From Indiana'], 'Lilly': ['Good GPA', 'Purdue grad', 'From Indiana', 'Little work experience', 'Volunteer'], 'Mohamed': ['Good GPA', 'Grad degree', 'From Indiana'], 'Maria': ['Good GPA', 'Purdue grad', 'From Indiana', 'Little work experience', 'Volunteer']}


iRatings = [i[1] for i in list(itemRatings.items())]
print("All items rated & tagged.")
print("Ratings span from " + str(round((min(iRatings)+1)/0.2, 1)) + " to " + str(round((max(iRatings)+1)/0.2,1)) + ".")
print("Here are all tags and their affiliated items: ")
tagPool = []
for i in tags.keys():
    for t in tags[i]:
        tagPool.append(t)
tagPool = list(set(tagPool))

# Tag-level ratings, weights, utilities
tagRatings = {}
tagWeights = {}
tagSigs = {}
tagUtilities = {}
# items affiliated with each tag (lined up with the indexes of tagPool)
affiliated = []
for t in tagPool:
    tagRatings[t] = 0
    tagWeights[t] = 0
    tagSigs[t] = 0
    tagUtilities[t] = 0
    af = []
    for i in tags.keys():
        if t in tags[i]:
            af.append(i)
    affiliated.append(af)
    # Displaying tags and their items to the user
    print("• " + t + ": " + str(af))
print()
cont = "untouched"
while(cont != ""):
    cont = input("Press Enter to continue")



# For each tag:
for t in range(len(tagPool)):
    tag = tagPool[t]
    # Skip if there are not enough items that the tag applies to:
    if len(affiliated[t])<2: continue
    tagRate = 0
    Rt = []
    for a in affiliated[t]:
        Rt.append(itemRatings[a])
        tagRate += itemRatings[a]
#   Skip if tag does not have a statistically significant preference
    w,p = wilcoxon(Rt)
    if p > 0.05: continue
# 	Calculate Inferred set(tag)-level rating
    tagRate = tagRate*(1/len(affiliated[t]))
    tagRatings[tag] = tagRate
# 	Calculate weight for tag
    weight = tagRate - NEUTRAL
    tagWeights[tag] = weight
# 	Calculate tag coverage
    tagCov = min((len(affiliated[t])/(seen.count(1))),((seen.count(1)-len(affiliated[t]))/(seen.count(1))))
# 	Calculate tag significance
    variance = np.var(Rt) if np.var(Rt) > 0 else 0.0000001
    tagSig = min(2, (abs(weight)/(variance/(len(affiliated[t])**(0.5)))))
    tagSigs[tag] = tagSig
# 	Calculate tag utility
    tagUtil = tagCov*tagSig*abs(weight)
    tagUtilities[tag] = tagUtil


# generating pairwise tags
pairwiseRatings = np.zeros((len(tagPool), len(tagPool)))
pairwiseWeights = np.zeros((len(tagPool), len(tagPool)))
pairwiseUtilities = np.zeros((len(tagPool), len(tagPool)))
pairwiseInter = [[[] for i in range(len(tagPool))] for i in range(len(tagPool))]
# List containing the pairwise tags that are affiliated with enough items to be usable
usables = []

# Calculating pairwise tag info
for a in range(len(tagPool)):
    for b in range(len(tagPool)):
        if a==b: continue
        tagA = tagPool[a]
        tagB = tagPool[b]
        pTag = tagA+"-"+tagB
        # intersection of all items rated by tag A and tag B
        inter = []
        for i in affiliated[a]:
            if i in affiliated[b]:
                inter.append(i)
        # If there are less than two items with both tags, skip pairwise tag
        if len(inter)<2: continue
        pairwiseInter[a][b]=inter
        # Calculating pairwise rating
        pairRate = 0
        Rab = []
        for i in inter:
            Rab.append(itemRatings[i])
            pairRate += itemRatings[i]
        #Wilcoxon test
        w,p = wilcoxon(Rab)
        if p > 0.05: continue
        usables.append([a,b])
        pairRate = (1/len(inter))*pairRate
        pairwiseRatings[a][b] = pairRate
        tagRatings[pTag] = pairRate
        #Calculating pairwise weight
        pairWeight = pairRate - tagWeights[tagA]
        pairwiseWeights[a][b] = pairWeight
        tagWeights[pTag] = pairWeight
        # Calculating pairwise coverage
        pairCov = min((len(inter)/len(affiliated[a])),((len(affiliated[a])-len(inter))/len(affiliated[a])))
        # Calculating pairwise significance
        variance = np.var(Rab) if np.var(Rab) > 0 else 0.0000001
        pairSig = min(2, abs(pairWeight)/(variance/(len(inter)**0.5)))
        tagSigs[pTag]=pairSig
        # Calculating pairwise utility
        pairUtil = tagUtilities[tagA] + pairCov*pairSig*abs(pairWeight)
        pairwiseUtilities[a][b] = pairUtil


def naturalize(tags, ratings):
    """
    Inputs: 
    - list 'tags': [tag] if single tag, [tagA, tagB, tagAB] if pairwise
    - list 'ratings': [rating] if single tag, [ratingA, ratingB, ratingAB] if pairwise
    
    Outputs:
    - String containing statement in natural language about tag relationship.
    """
    # statement formats
    single = "You {strength}{like}like candidates tagged with '{tag}.'"
    espIf = "You {strength}{like}like candidates tagged as '{tag1},' especially if also tagged as '{tag2}.'"
    espIfNot = "You {strength}{like}like candidates tagged as '{tag1},' especially if they are not also tagged as '{tag2}.'"
    unless = "You {strength}{like}like candidates tagged as '{tag1}' unless they are also tagged as '{tag2}.'"
    exist = "You only {strength}{like}like candidates tagged as '{tag1}' if the candidate is also tagged as '{tag2}.'"
    noStatSingle = "You have no statistically significant preference for candidates tagged as '{tag}.'"
    noStatPair = "You have no statistically significant preference for candidates tagged as both '{tag1}' and '{tag2}.'"
    if len(tags)==1:
        strength = ""
        like = ""
        # Determining tag sentiment
        if ratings[0] < 0:
            like = "dis"
        if ratings[0] == 0:
            return noStatSingle.format(tag=tags[0]),"NA"
        # Determining strength
        if (ratings[0]>0.5) or (ratings[0]<-0.5):
            strength = "strongly "
        return single.format(strength=strength, like=like, tag=tags[0]), like
    else:
        strength = ""
        like = ""
        # Determining tag sentiment
        if ratings[0] < 0:
            like = "dis"
        if sum(ratings)==0:
            return noStatPair.format(tag1=tags[0], tag2=tags[1]), "NA"
        # Assigning statement
        if (np.sign(ratings[2])==np.sign(ratings[0])) and (abs(ratings[2]) > abs(ratings[0]))and not (-0.1 <= ratings[0] <= 0.1):
            return espIf.format(strength=strength, like=like, tag1=tags[0], tag2=tags[1]), like
        elif (np.sign(ratings[2])==np.sign(ratings[0])) and (abs(ratings[0]) > abs(ratings[2])) and not(-0.1 <= ratings[0] <= 0.1):
            return espIfNot.format(strength=strength, like=like, tag1=tags[0], tag2=tags[1]), like
        elif (np.sign(ratings[2])!=np.sign(ratings[0])) and not(-0.1 <= ratings[0] <= 0.1):
            return unless.format(strength=strength, like=like, tag1=tags[0], tag2=tags[1]), like
        elif (-0.11 <= ratings[0] <= 0.11) and not (-0.11 <= ratings[2] <= 0.11):
            like = "" if ratings[2] > 0 else "dis"
            return exist.format(strength=strength, like=like, tag1=tags[0], tag2=tags[1]), like
        else:
            return "Your opinion of a candidate tagged as '{tag1}' does not seem to change when that candidate is also tagged as '{tag2}.'".format(tag1=tags[0],tag2=tags[1]), like

# Getting all usable tags to evaluate for statements
statements = []
for t in range(len(tagPool)):
    statements.append([t])
for pt in usables:
    statements.append(pt)

# Select top k statements for the user
topK = []
topK_util = []
# Mutable list of lists where a single tag is [<tagPool index>] and a pairwise tag is  [<tagPool index for tag 1>, <tagPool index for tag 2>]
sMutable = [s for s in statements]
# list of items associated with the topK statements
I_sk = []
for i in range(K):
    if len(sMutable)==0: break
    # Calculating first utility to start search for maximum
    tag = ""
    sig0 = 0
    if len(sMutable[0]) ==1:
        tag = tagPool[sMutable[0][0]]
        sig0 = tagSigs[tag]
        Istar_s0 = affiliated[sMutable[0][0]]
    else:
        tag = tagPool[sMutable[0][0]]+"-"+tagPool[sMutable[0][1]]
        sig0 = tagSigs[tag]
        #Calculating coverage
        Istar_s0 = pairwiseInter[sMutable[0][0]][sMutable[0][1]]
    cardIstar = sum(seen)
    disjoint = [i for i in Istar_s0 if i not in I_sk]
    cov0 = min((len(disjoint)/cardIstar), (cardIstar-len(disjoint))/cardIstar)
    weight0 = tagWeights[tag]
    util0 = cov0*sig0*abs(weight0)
    # Keeping track of statement with maximum utility, initializing with the first statement in the list
    argmax = util0
    maxInd = 0
    max_items = Istar_s0
    # For each of the other statements
    for s in range(1, len(sMutable)):
        tag = ""
        cov = 0
        sig = 0
        # If statement tag is single
        if len(sMutable[s]) ==1:
            tag = tagPool[sMutable[s][0]]
            sig = tagSigs[tag]
            Istar_s = affiliated[sMutable[s][0]]
        # If statement tag is pairwise
        else:
            tag = tagPool[sMutable[s][0]]+"-"+tagPool[sMutable[s][1]]
            sig = tagSigs[tag]
            Istar_s = pairwiseInter[sMutable[s][0]][sMutable[s][1]]
        # Calculating coverage
        disjoint = [i for i in Istar_s if i not in I_sk]
        cov = min((len(disjoint)/cardIstar), (cardIstar-len(disjoint))/cardIstar)
        weight = tagWeights[tag]
        util = cov*sig*abs(weight)
        # Checking to see if this has higher utility than current max
        if util > argmax: 
            maxInd = s
            argmax = util
            max_items = Istar_s
    # Recording max for this round, deleting it from next round's potential candidates
    topK.append(sMutable[maxInd])
    topK_util.append(argmax)
    for i in max_items: I_sk.append(i)
    del sMutable[maxInd]

nls = []

# For each of the k statements:
for k in topK:
    pairwise = False
    single = False
    if len(k)==1:
        single = k[0]
    else:
        pairwise = [k[0],k[1]]
# 	Generate natural language representation of statement
    ts = [tagPool[k[0]]] if len(k)==1 else [tagPool[pairwise[0]], tagPool[pairwise[1]], tagPool[pairwise[0]]+"-"+tagPool[pairwise[1]]]
    rs = [tagRatings[t] for t in ts]
    nlStatement = naturalize(ts, rs)

# 	Select representative example
    example = ""
    like = True if nlStatement[1] == "" else False
    if len(k)==1: 
        choices = affiliated[single]
        if like:
            choice = choices[0]
            argmax = itemRatings[choices[0]]
            for c in choices:
                if itemRatings[c] > argmax: 
                    argmax = itemRatings[c]
                    choice = c
        else:
            choice = choices[0]
            argmin = itemRatings[choices[0]]
            for c in choices:
                if itemRatings[c] < argmin: 
                    argmin = itemRatings[c]
                    choice = c
        example = choice
    else: 
        if "especially if they are not" in nlStatement[0]:
            tagAitems = affiliated[pairwise[0]]
            tagBitems = affiliated[pairwise[1]]
            choices = []
            for a in tagAitems:
                if a not in tagBitems: choices.append(a)
            if len(choices)==0: continue
        else:
            choices = pairwiseInter[pairwise[0]][pairwise[1]]
        if like:
            choice = choices[0]
            argmax = itemRatings[choices[0]]
            for c in choices:
                if itemRatings[c] > argmax: 
                    argmax = itemRatings[c]
                    choice = c
        else:
            choice = choices[0]
            argmin = itemRatings[choices[0]]
            for c in choices:
                if itemRatings[c] < argmin: 
                    argmin = itemRatings[c]
                    choice = c
        example = choice
    finalStatement = nlStatement[0]+" Example: "+example
    nls.append(finalStatement)

# Show statements to user 
print()
print("*"*31)
print("** Summary of User Interests **")
print("*"*31)
count = 0
print("(Utility): Statement")
for s in nls:
    print(str(round(topK_util[count],2))+": " + s)
    count +=1

print()
cont = "untouched"
while(cont != ""):
    cont = input("Press Enter to continue")
print()

likelihoods = {}
topK_strings = [tagPool[topK[i][0]] if len(topK[i])==1 else tagPool[topK[i][0]]+"-"+tagPool[topK[i][1]] for i in range(len(topK))]

# Calculate user likelihood for each item
# For each seen item:
for i in range(len(items)):
    if seen[i] == 0:
        continue
    # Initialize item-tag vector
    T_i = tags[items[i]]
    w_t = [1 if tagPool[j] in T_i else 0 for j in range(len(tagPool))]
    
    tPlus = []
    tMinus = []
    for t in topK_strings:
        if tagWeights[t] > 0: tPlus.append(t)
        else: tMinus.append(t)
    likelihood = 0
    # for each tag in tPlus
    for t in tPlus:
        # Calculate logP(t|theta_i)
        w_ti = 0
        if not ("-" in t):
            tagIndex = tagPool.index(t)
            w_ti = w_t[tagIndex]
        else: 
            t1,t2 = t.split("-")
            tagIndex1 = tagPool.index(t1)
            tagIndex2 = tagPool.index(t2)
            if w_t[tagIndex1]==1 and w_t[tagIndex2]==1:
                w_ti=1
        p_tthetai = (w_ti + MU*len(affiliated[tagIndex])/sum(seen))/(MU+sum(seen)/len(affiliated[tagIndex]))
        # Get wtu+
        wtu_plus = tagWeights[t]
        # Add to user likelihood
        likelihood+= wtu_plus*math.log(p_tthetai)
    # for each tag in tMinus
    for t in tMinus:
        # Calculate logP(t|theta_i)
        w_ti = 0
        if not ("-" in t):
            tagIndex = tagPool.index(t)
            w_ti = w_t[tagIndex]
        else: 
            t1,t2 = t.split("-")
            tagIndex1 = tagPool.index(t1)
            tagIndex2 = tagPool.index(t2)
            if w_t[tagIndex1]==1 and w_t[tagIndex2]==1:
                w_ti=1
        p_tthetai = (w_ti + MU*len(affiliated[tagIndex])/sum(seen))/(MU+sum(seen)/len(affiliated[tagIndex]))
        # Get wtu-
        wtu_minus = tagWeights[t]
        # Subtract from user likelihood (already negative bc of wtu_minus)
        likelihood= wtu_minus*math.log(p_tthetai)
    # assign likelihood to item
    likelihoods[items[i]] = likelihood
# Rank items by likelihood
ranked = [i for i in likelihoods.keys()]
ranked.sort(key=lambda x: likelihoods[x], reverse=True)

# Recommend items according to calculations
print()
print("*"*31)
print("** Candidate Recommendations **")
print("*"*31)
print("Rank: Candidate (Likelihood)")
for i in range(1, len(ranked)+1):
    print(str(i)+": "+ranked[i-1] + " (" + str(round(likelihoods[ranked[i-1]],2))+")")

# Nothing changes until user either wants to make changes to the weights, or they decide to rate or tag more items

