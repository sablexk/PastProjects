# -*- coding: utf-8 -*-
"""
Created on Sun May 17 13:28:59 2020

@author: sstan
"""


import re
import csv
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from random import randint

defaultStopwords = stopwords.words('english')

# remove punctuation first
# tokenizer = RegexpTokenizer(r"[\w+")
# no_punct_origin = tokenizer.tokenize(raw_origin)
# no_punct_sherlock = tokenizer.tokenize(raw_sherlock)

def get_random_ints(num_ints, max_num, other_set):
    setOfRandomInts = set()
    while len(setOfRandomInts) < num_ints:
        rNum = randint(0, max_num)
        if(rNum not in other_set):

            setOfRandomInts.add(rNum)
            
    return(setOfRandomInts)

with open("cleanReviewsFile.csv", 'r') as csvfile:
    csvreader  = csv.DictReader(csvfile, delimiter=',')
    print(csvreader.fieldnames)
    
    allNegativeReviews = []    
    allPositiveReviews = []
    for review in csvreader:
        if review['Rating'] == "5":
            allPositiveReviews.append(review)
        if review['Rating'] == "1":
            allNegativeReviews.append(review)
    
    posN = 500
    negN = 500
    
    posTestingSelector = get_random_ints(100, len(allPositiveReviews), [])
    posTrainingSelector = get_random_ints(posN-100, len(allPositiveReviews), posTestingSelector)
    
    negTestingSelector = get_random_ints(100, len(allNegativeReviews), [])
    negTrainingSelector = get_random_ints(negN-100, len(allNegativeReviews), negTestingSelector)

    testingPos = []
    trainingPos = []

    for i in range(0, len(allPositiveReviews)):
        if i in posTestingSelector:
            testingPos.append(allPositiveReviews[i]['Review Text'])
        if i in posTrainingSelector:
            trainingPos.append(allPositiveReviews[i]['Review Text'])
       
    
    testingNeg = []
    trainingNeg = []

    for i in range(0, len(allNegativeReviews)):
        if i in negTestingSelector:
            testingNeg.append(allNegativeReviews[i]['Review Text'])
        if i in negTrainingSelector:
            trainingNeg.append(allNegativeReviews[i]['Review Text']) 
    



    # there are 2 postive and 3 negative in the training
    total = len(trainingPos) + len(trainingNeg)
    ProbPos = len(trainingPos) / total
    ProbNeg  = len(trainingNeg) / total
    
    newPosTraining = trainingPos
    newNegTraining = trainingNeg
    
    # newPosTraining = []
    # newNegTraining = []
    
    
    
    # for s in trainingPos:
    
    #     new = ''
    
    #     tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    #     noPunct = tokenizer.tokenize( s )
    
    #     for word in noPunct:
    
    #         if word.lower() not in defaultStopwords:
    #             new += word.lower()
    #             new += ' '
    
    #     newPosTraining.append(new)
    
    
    # for s in trainingNeg:
    
    #     new = ''
    #     tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    #     noPunct = tokenizer.tokenize( s )
    
    #     for word in noPunct:
           
    #         if word.lower() not in defaultStopwords:
    #             new += word.lower()
    #             new += ' '
    
    #     newNegTraining.append(new)
    
        
    
    def get_word_count(word, dictionary):
        if word in dictionary:
            return dictionary[word]
        else:
            return 0
    
    V = set()
    bagPos = {}   # bagPos: words in "positive" class
    for s in newPosTraining:
        ts = nltk.word_tokenize(s)
        print(ts)
        for w in ts:
            if w in bagPos:
                bagPos[w] +=1
            else:
                bagPos[w] =1
            V.add(w)
    
    bagNeg = {}   # bagNeg: words in "negative" class
    for s in newNegTraining:
    	ts = nltk.word_tokenize(s)
    	for w in ts:
    		if w in bagNeg:
    			bagNeg[w] +=1
    		else:
    			bagNeg[w] =1
    		V.add(w)
            
    true_pos = 0
    false_neg = 0
    for fullTestString in testingPos:
        # print("\n\nTest document = " + fullTestString)
        fullTestList = nltk.word_tokenize(fullTestString)
        test = [ w for w in fullTestList if w in V]     
        
        likelihoodW_Pos = {} 
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagPos) + 1)
    
        for w in test:
         	likelihoodW_Pos[w] =  (get_word_count(w, bagPos) + 1) / denominator
     
        likelihoodW_Neg = {} # dictionary of probabilities for negative class
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagNeg) + 1)
    
        for w in test:
         	likelihoodW_Neg[w] =  (get_word_count(w, bagNeg) + 1) / denominator
    
        finalProbNeg = ProbNeg 
        for w in test:
         	finalProbNeg *=  likelihoodW_Neg[w]
    
        finalProbPos = ProbPos 
        for w in test:
         	finalProbPos *=  likelihoodW_Pos[w]
      
        if (finalProbPos > finalProbNeg):
            true_pos += 1
            print("\nModel predicts the test query belongs in the POSITIVE class")
        else:
            false_neg += 1
            print("\nModel predicts the test query belongs in the NEGATIVE class")
    
    true_neg =0
    false_pos = 0        
    for fullTestString in testingNeg:
        # print("\n\nTest document = " + fullTestString)
        fullTestList = nltk.word_tokenize(fullTestString)
        test = [ w for w in fullTestList if w in V]     
        
        likelihoodW_Pos = {} 
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagPos) + 1)
    
        for w in test:
         	likelihoodW_Pos[w] =  (get_word_count(w, bagPos) + 1) / denominator
     
        likelihoodW_Neg = {} # dictionary of probabilities for negative class
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagNeg) + 1)
    
        for w in test:
         	likelihoodW_Neg[w] =  (get_word_count(w, bagNeg) + 1) / denominator
    
        finalProbNeg = ProbNeg 
        for w in test:
         	finalProbNeg *=  likelihoodW_Neg[w]
    
        finalProbPos = ProbPos 
        for w in test:
         	finalProbPos *=  likelihoodW_Pos[w]
      
        if (finalProbPos > finalProbNeg):
            false_pos += 1
            print("\nModel predicts the test query belongs in the POSITIVE class")
        else:
            true_neg += 1
            print("\nModel predicts the test query belongs in the NEGATIVE class")
    
    print("\ntrue_pos = " + str(true_pos))
    print("\nfalse_neg = " + str(false_neg))
    print("\ntrue_neg = " + str(true_neg))
    print("\nfalse_pos = " + str(false_pos))
    
    positive_recall = true_pos/ (true_pos + false_neg)

    positive_precision = true_pos / (true_pos  + false_pos )
    
    negative_recall = true_neg / (true_neg  + false_pos )
    
    negative_precision = true_neg / (true_neg  + false_neg )
    
    accuracy = (true_pos  +true_neg )/(true_pos  +true_neg  +false_neg  + false_pos )
    
    print("positive recall: " + str(positive_recall))
    print("positive precision: " + str(positive_precision))
    print("negative recall: " + str(negative_recall))
    print("negative precision: " + str(negative_precision))
    print("accuracy: " + str(accuracy))
