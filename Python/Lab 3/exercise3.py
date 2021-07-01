# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 09:17:45 2020

@author: sstan
"""

import re
# Create the two sets of male/female words
# If you add to one set, make sure you add the equivalent paired word to the other 
# set to maintain balance.
maleWords = set( [ 
'he','him','his','himself','man','men',"men's",'guy','boy','boys','boyfriend',
'boyfriends','brother','brothers','dad','dads','father','fathers','grandfather',
'grandpa','grandson','husband','husbands','male','mr','nephew','newphews',
'son','sons','uncle','uncles','widower','widowers','gentleman','gentlemen'] )

femaleWords = set( [ 
'she','her','hers','herself','woman','women',"women's",'gal','girl','girls','girlfriend',
'girlfriends','sister','sisters','mom','moms','mother','mothers','grandmother',
'grandma','granddaughter','wife','wives','female','mrs','ms','neice','neices',
'daughter','daughters','aunt','aunts','widow','widows','lady','ladies'] )

HeadlinesMale = set()
HeadlinesFemale = set()
maleWordCounter = {}
femaleWordCounter = {}


CFemNotMale_N = set()
CMCMaleNotFem_N = set()

debug = False    # if set to True will print out debugging statments
# open and read from a file
with open("./abcnews-date-text.csv",'r') as fp:     # full file of 1M lines
# with open("./abcnews-date-text-short.csv",'r') as fp:   # first 5000 lines of full 
    
    line = fp.readline()
    #print(line)
    count = 0
    while line:
        # Cleaning: remove the number and comma at the start of each line and make lower case
        commaReplaced = re.sub(r',', ' ', line) # replace the comma with a space
        asList = re.split('\s',commaReplaced)  # split the line into a list
        asList.pop(0)   # remove the first list element (which is a number)
        asListLower = [e.lower() for e in asList]   # make lower case
        
        #go word by word in search of male/female words, add to respective sets
        for word in asListLower:
            if word in maleWords:
                HeadlinesMale.add(line[9:]) #do 9: to strip away date + comma (aka substring)
            if word in femaleWords:
                HeadlinesFemale.add(line[9:]) #do 9: to strip away date + comma (aka substring)

        count = count + 1
        line = fp.readline()

#get all words from male headlines & put in dictionary + count occurances
for line in HeadlinesMale:
    commaReplaced = re.sub(r',', '', line) # replace the comma with a space
    asList = re.split('\s',commaReplaced)  # split the line into a list
    for word in asList:
        if word in maleWordCounter:
            maleWordCounter[word] = maleWordCounter[word] + 1
        else:
            maleWordCounter[word] = 1

#get all words from female headlines & put in dictionary + count occurances
for line in HeadlinesFemale:
    commaReplaced = re.sub(r',', ' ', line) # replace the comma with a space
    asList = re.split('\s',commaReplaced)  # split the line into a list
    for word in asList:
        if word in femaleWordCounter:
            femaleWordCounter[word] = femaleWordCounter[word] + 1
        else:
            femaleWordCounter[word] = 1
            
maleWordCounter.pop('')
femaleWordCounter.pop('')
#find most common words in fe/male headlines (aka sort the dictionaries)    
CMale_N = dict(sorted(maleWordCounter.items(), key = lambda kv:(kv[1], kv[0]), reverse = True))
CFemale_N = dict(sorted(femaleWordCounter.items(), key = lambda kv:(kv[1], kv[0]), reverse = True))
   
#get rid of the counts; keep only the keys aka the words
CMale_N = list(CMale_N.keys())
CFemale_N = list(CFemale_N.keys())


#get top 10, 20, 30, 60 fe/male; put each in separate lists to compare later
CMale_10 = CMale_N[:10]
CMale_20 = CMale_N[:20]
CMale_30 = CMale_N[:30]
CMale_60 = CMale_N[:60]

CFemale_10 = CFemale_N[:10]
CFemale_20 = CFemale_N[:20]
CFemale_30 = CFemale_N[:30]
CFemale_60 = CFemale_N[:60]


#words in male but not in female: CMaleNotFem_N (male - female)
CMaleNotFem_10 = set(CMale_10).difference(set(CFemale_10))
CMaleNotFem_20 = set(CMale_20).difference(set(CFemale_20))
CMaleNotFem_30 = set(CMale_30).difference(set(CFemale_30))
CMaleNotFem_60 = set(CMale_60).difference(set(CFemale_60))

#words in female but not in male: CFemNotMale_N (female - male)
CFemNotMale_10 = set(CFemale_10).difference(set(CMale_10))
CFemNotMale_20 = set(CFemale_20).difference(set(CMale_20))
CFemNotMale_30 = set(CFemale_30).difference(set(CMale_30))
CFemNotMale_60 = set(CFemale_60).difference(set(CMale_60))


print("CMaleNotFem_10:\n", CMaleNotFem_10, "\n")
print("CFemNotMale_10:\n", CFemNotMale_10, "\n")
print("CMaleNotFem_30:\n", CMaleNotFem_30, "\n")
print("CFemNotMale_30:\n", CFemNotMale_30, "\n")
print("CMaleNotFem_60:\n", CMaleNotFem_60, "\n")
print("CFemNotMale_60:\n", CFemNotMale_60, "\n")