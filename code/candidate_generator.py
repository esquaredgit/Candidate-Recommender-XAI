"""
CSCI-B659 Final Project, Ethan Eldridge

This is code I used to generate the distribution of candidates and their ratings/tags for the experiment. 
It is as randomized as it can be while still maintaining the desired distribution of tags.
"""

import random as rn

items = ["Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Charlotte", "William", "Sophia", "James", "Amelia", "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Evelyn", "Alexander", "Harper", "John", "Mary Katherine", "David", "Kayla", "Nathan", "Stella", "Maximilian", "Lilly", "Mohamed", "Maria"]
tags = [[] for i in range(len(items))]
ratings = [0 for i in range(len(items))]

strongLiked = rn.sample(items, 10)
remainder = [name for name in items if not (name in strongLiked)]
liked = rn.sample(remainder, 10)
disliked = [name for name in remainder if not (name in liked)]



# I like candidates tagged with 'good GPA'
# I like candidates tagged with 'good GPA,' especially if they are also tagged as 'graduate degree.'
goodGPA = [l for l in liked]
for s in strongLiked: goodGPA.append(s) 

graduateDegree = [s for s in strongLiked] #10 strongly liked from GPA

# I dislike candidates tagged with 'bad GPA.'
badGPA = [d for d in disliked] #10 disliked

# I like candidates tagged with 'from Indiana,' especially if they are NOT tagged as 'Purdue University'
purdue = [l for l in liked] # 10 less-liked from Indiana
fromIndiana = [p for p in purdue] # 20 strongly liked

# I don't like candidates tagged with 'little work experience' unless they are also tagged as 'volunteer.'
littleWorkExp = [] #20 disliked
volunteer = [] #10 liked from LWE 

for b in badGPA: littleWorkExp.append(b)
grad_vols = rn.sample(graduateDegree, 5)
for g in grad_vols:
    littleWorkExp.append(g)
    volunteer.append(g)
purdue_vols = rn.sample(purdue, 5)
for p in purdue_vols:
    littleWorkExp.append(p)
    volunteer.append(p)

grad_rest = [g for g in graduateDegree if not (g in grad_vols)]
for g in grad_rest: fromIndiana.append(g)

assert len(graduateDegree) == 10
assert len(badGPA) == 10
assert len(purdue) == 10
assert len(goodGPA) == 20
assert len(fromIndiana) == 15
assert len(volunteer) == 10
assert len(strongLiked) == 10
assert len(liked) == 10
assert len(disliked) == 10

# Assigning tags
for g in goodGPA:
    tags[items.index(g)].append("Good GPA")
for d in graduateDegree:
    tags[items.index(d)].append("Grad degree")
for b in badGPA:
    tags[items.index(b)].append("Bad GPA")
for p in purdue:
    tags[items.index(p)].append("Purdue grad")
for i in fromIndiana: 
    tags[items.index(i)].append("From Indiana")
for l in littleWorkExp:
    tags[items.index(l)].append("Little work experience")
for v in volunteer:
    tags[items.index(v)].append("Volunteer")

# Assigning Ratings
for s in strongLiked:
    rate = rn.uniform(0.6, 1)
    ratings[items.index(s)] = rate
for l in liked:
    rate = rn.uniform(0.2, 0.49)
    ratings[items.index(l)] = rate
for d in disliked:
    rate = rn.uniform(-0.5, 0)
    ratings[items.index(d)] = rate

tagDict = {}
itemRatings = {}
for i in range(len(items)):
    print("• " + items[i] + " (" + str(round(ratings[i],2)) + "): " + str(tags[i]))
    tagDict[items[i]] = tags[i]
    itemRatings[items[i]] = ratings[i]

# Copy and paste these results into the main file to start
print()
print(tagDict)
print()
print(itemRatings)
