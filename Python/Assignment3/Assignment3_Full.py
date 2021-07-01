# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:44:58 2020

@author: sstan
"""


import re
import csv
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from random import randint
from queue import Queue
from math import exp, log
from random import random, randint
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics import confusion_matrix
defaultStopwords = stopwords.words('english')   # can get other languages
debug = False

#Various Functions to be Called-----

def get_random_ints(num_ints, max_num, other_set):
    setOfRandomInts = set()
    while len(setOfRandomInts) < num_ints:
        rNum = randint(0, max_num)
        if(rNum not in other_set):

            setOfRandomInts.add(rNum)
            
    return(setOfRandomInts)

#--------  function to calculate z =>  Equation 5.2
def zValue(fv,w,b):
    if (len(fv) != len(w)):
        print("ERROR, length mismatch, exiting...")
        exit()
    z = 0
    for i in range(0,len(fv)):
        z += fv[i] * w[i]
    z += b
    return(z)


#--------  function to sigmoid =>  Equation 5.4
def sigma(z):
    try:
        sig = exp(-z)
    except:
        print("PROBLEM in sigma()")
        print(z)
        if (z < 0):
            return(1)
    return( 1.0 / (1 + exp(-z)))


#--------  function to cross entropy loss  =>  Equation 5.11
def getLCE(x,w,b,y):
# LCE = -1 * ( y*log(sigma(zValue(x,w,b))) + (1-y)*log( 1 - sigma(zValue(x,w,b))))
# But - if sigma returns 1, then 2nd log is not defined even though the term will be set 
#      to zero by (1-y).  So, lets split into the two parts
    z = zValue(x,w,b)
    sig = sigma(z)
    if (y == 1):
        # LCE = -1 * ( y*log(sigma(zValue(x,w,b))) )
        if (sig == 0):
            LCE = 1
        else:
            LCE = -1 * log(sigma(z)) 
    else:
        # LCE = -1 * ( (1-y)*log( 1 - sigma(zValue(x,w,b))))
        if (sig == 1):
            LCE = 0
        else:
            LCE = -1 *  log( 1 - sigma(z))
    return(LCE)

y=0
#---------------  function to do one iteration of gradient descent
def doOneIteration(eta):
# uses and modifies global vars theta[], w[], and b
# takes in parameter eta
    global theta
    global w, b
    global x
    global grad 

    #calculate gradients
    grad[0] = x[0] * ( sigma(zValue(x,w,b)) - y )
    grad[1] = x[1] * ( sigma(zValue(x,w,b)) - y )
    grad[2] = x[2] * ( sigma(zValue(x,w,b)) - y )
    grad[3] = ( sigma(zValue(x,w,b)) - y )

    #update theta
    theta[0] = theta[0] - (eta * grad[0] )
    theta[1] = theta[1] - (eta * grad[1] )
    theta[2] = theta[2] - (eta * grad[2] )
    theta[3] = theta[3] - (eta * grad[3] )

    #update w and b
    w[0] = theta[0]
    w[1] = theta[1]
    w[2] = theta[2]
    b = theta[3]

grad = []
def avgGrad():
    if debug:
        print('entering avgGrad')
    count = 0 
    total = 0
    for i in grad:
        total += abs(i)  # absolute value
        count += 1
    if debug:
        print("leaving avgGrad, total&count = " + str(total) + str(" ") + str(count))
    return( total / count)


def createFeatureVector(s, wordsPositive, wordsNegative):
    fv = [0,0,0]
    tokens = nltk.word_tokenize(s)
    for word in tokens:
        if word in wordsPositive:
            fv[0] += 1
        if word in wordsNegative:
            fv[1] += 2
    fv[2] = 0.01 * len(s) 
    return(fv)

#--------------------------------

    
with open("cleanReviewsFile.csv", 'r') as csvfile:
    csvreader  = csv.DictReader(csvfile, delimiter=',')
    
    FiveStarReviews = []    
    OneStarReviews = []
    for review in csvreader:
        if review['Rating'] == "5":
            FiveStarReviews.append(review)
        if review['Rating'] == "1":
            OneStarReviews.append(review)
    
    posN = 800
    negN = 800
    
    posTestingSelector = get_random_ints(100, len(FiveStarReviews), [])
    posTrainingSelector = get_random_ints(posN-100, len(FiveStarReviews), posTestingSelector)
    
    negTestingSelector = get_random_ints(100, len(OneStarReviews), [])
    negTrainingSelector = get_random_ints(negN-100, len(OneStarReviews), negTestingSelector)

    testingPos = []
    trainingPos = []

    for i in range(0, len(FiveStarReviews)):
        if i in posTestingSelector:
            testingPos.append(FiveStarReviews[i]['Review Text'])
        if i in posTrainingSelector:
            trainingPos.append(FiveStarReviews[i]['Review Text'])
       
    
    testingNeg = []
    trainingNeg = []

    for i in range(0, len(OneStarReviews)):
        if i in negTestingSelector:
            testingNeg.append(OneStarReviews[i]['Review Text'])
        if i in negTrainingSelector:
            trainingNeg.append(OneStarReviews[i]['Review Text']) 

#HAND CODED NAIVE BAYES
            
            
total = len(trainingPos) + len(trainingNeg)
ProbPos = len(trainingPos) / total
ProbNeg  = len(trainingNeg) / total

newPosTraining = trainingPos
newNegTraining = trainingNeg

def get_word_count(word, dictionary):
    if word in dictionary:
        return dictionary[word]
    else:
        return 0

V = set()
bagPos = {}   # bagPos: words in "positive" class
for s in newPosTraining:
    ts = nltk.word_tokenize(s)
    #print(ts)
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
        #print("\nModel predicts the test query belongs in the POSITIVE class")
    else:
        false_neg += 1
        #print("\nModel predicts the test query belongs in the NEGATIVE class")

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
        #print("\nModel predicts the test query belongs in the POSITIVE class")
    else:
        true_neg += 1
        #print("\nModel predicts the test query belongs in the NEGATIVE class")

# print("\ntrue_pos = " + str(true_pos))
# print("\nfalse_neg = " + str(false_neg))
# print("\ntrue_neg = " + str(true_neg))
# print("\nfalse_pos = " + str(false_pos))

positive_recall = true_pos/ (true_pos + false_neg)

positive_precision = true_pos / (true_pos  + false_pos )

negative_recall = true_neg / (true_neg  + false_pos )

negative_precision = true_neg / (true_neg  + false_neg )

accuracy = (true_pos  +true_neg )/(true_pos  +true_neg  +false_neg  + false_pos )

print("HAND CODED NAIVE BAYES")
print("positive recall: " + str(positive_recall))
print("positive precision: " + str(positive_precision))
print("negative recall: " + str(negative_recall))
print("negative precision: " + str(negative_precision))
print("accuracy: " + str(accuracy))
print('\n')
print('\n')
print('---------------')




#HAND CODED LOGISTIC REGRESSION
        
        
wordsPositive = set()
fpp = open("positive-words.txt",mode='r',encoding="ISO-8859-1")
for line in fpp:
    aStr = line.replace('\n','')
    wordsPositive.add(aStr)

# create set of wordsNegative by reading in from file
wordsNegative = set()
fpn = open("negative-words.txt",mode='r',encoding="ISO-8859-1")
for line in fpn:
    aStr = line.replace('\n','')
    line.replace('\n','')
    wordsNegative.add(aStr)

posTrainStrings = []
negTrainStrings = []

for review in trainingPos:
    new = ''
    tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    noPunct = tokenizer.tokenize( review )
    for word in noPunct:
#         if word.lower() not in defaultStopwords:    
        new += word.lower()
        new += ' ' 
    posTrainStrings.append(new)
    
for review in trainingNeg:
    new = ''
    tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    noPunct = tokenizer.tokenize( review )
    for word in noPunct:
#         if word.lower() not in defaultStopwords:    
        new += word.lower()
        new += ' ' 
    negTrainStrings.append(new)
    
posFeatureVectors = []
for s in posTrainStrings:
      fv = createFeatureVector(s, wordsPositive, wordsNegative)
      posFeatureVectors.append(fv)

negFeatureVectors = []
for s in negTrainStrings:
      fv = createFeatureVector(s, wordsPositive, wordsNegative)
      negFeatureVectors.append(fv)
     
globalETA = 0.0001
w = [0, 0, 0]   # the three weight values that correspond to the feature vector and used in dot-product
b = 0  # bias adjustment
theta = [0,0,0,0]  # w and b combined, algorithm in book uses "theta" so we will follow
grad = [1,1,1,1]   # gradient 

iterationCount = 0  

while (iterationCount < 200000) and (avgGrad() > 0.001) :
    iterationCount += 1
    # pick a document feature vector at random
    # if ((iterationCount % 2) == 0):   # alternate neg/pos set, not sure which of alternating/random is better
    if (random() < 0.5):  # randomly choose from pos set
        rNum = randint(0,len(posFeatureVectors)-1)
        x = posFeatureVectors[rNum]
        y = 1  # tagged positive, so y = 1
    else:     # randomly choose from pos set
        rNum = randint(0,len(negFeatureVectors)-1)
        x = negFeatureVectors[rNum]
        y = 0  # tagged negative, so y = negative
    doOneIteration(eta = globalETA)

    LCE = getLCE(x,w,b,y)
    if (LCE < 0.0):
        print("ERROR: LCE = " + str(LCE) + ", exiting...." )
        print("x = " + str(x))
        print("w = " + str(w))
        print("b = " + str(b))
        print("y = " + str(y))
        print("exiting...." )
        exit()



posTestVectors = []
for s in testingPos:
    fv = createFeatureVector(s, wordsPositive, wordsNegative)
    posTestVectors.append(fv)

negTestVectors = []
for s in testingNeg:
    fv = createFeatureVector(s, wordsPositive, wordsNegative)
    negTestVectors.append(fv)

truePos = trueNeg = falsePos = falseNeg = 0



for fv in posTestVectors:

    z = zValue(fv,w,b)
    yPrime = sigma(z)

    if (yPrime > 0.5):
        truePos += 1
    else:
        falseNeg += 1



for fv in negTestVectors:

    z = zValue(fv,w,b)
    yPrime = sigma(z)

    if (yPrime > 0.5):

        falsePos += 1
    else:
        trueNeg += 1


positive_recall = truePos/ (truePos + falseNeg)
positive_precision = truePos/ (truePos + falsePos)
negative_recall = trueNeg/ (trueNeg + falsePos)
negative_precision = trueNeg/ (trueNeg + falseNeg)
accuracy = (truePos +trueNeg)/(truePos +trueNeg +falseNeg + falsePos)

print("ETA = " + str(globalETA) )
print("iterationCount = " + str(iterationCount))
print("HAND CODED LOGISTIC REGRESSION")
print("pos_recall = " + str(positive_recall))
print("pos_precision = " + str(positive_precision))
print("neg_recall = " + str(negative_recall))
print("neg_precision = " + str(negative_precision))
print("accuracy = " + str(accuracy))
print('\n')
print('\n')
print('---------------')
            
            
#SKLEARN NAIVE BAYES

newPosTraining = trainingPos
newNegTraining = trainingNeg

def get_word_count(word, dictionary):
    if word in dictionary:
        return dictionary[word]
    else:
        return 0


posTrainStrings = []
negTrainStrings = []
for review in trainingPos:
    new = ''
    tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    noPunct = tokenizer.tokenize( review )
    for word in noPunct:
#         if word.lower() not in defaultStopwords:    
        new += word.lower()
        new += ' ' 
    posTrainStrings.append(new)
    
for review in trainingNeg:
    new = ''
    tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    noPunct = tokenizer.tokenize( review )
    for word in noPunct:
#         if word.lower() not in defaultStopwords:    
        new += word.lower()
        new += ' ' 
    negTrainStrings.append(new)
        
labelPosDocs = [1 for i in posTrainStrings]
labelNegDocs = [0 for i in negTrainStrings]

# create one large list of the docs (order does not matter)
training = posTrainStrings + negTrainStrings

# create one large list of the labels (order should match the docs)
labels = labelPosDocs + labelNegDocs

cv = CountVectorizer()
cv.fit_transform(training)
counts = cv.transform(training)

posTestLabels = [1 for i in testingPos]
negTestLabels = [0 for i in testingNeg]

testLabels = posTestLabels + negTestLabels

combinedTests = testingPos + testingNeg
 
modelNB = MultinomialNB().fit(counts, labels)


testCounts = cv.transform(combinedTests)

probs = modelNB.predict_proba(testCounts)

truePos = falsePos = trueNeg = falseNeg = 0
for i in range(len(probs)):

    if (testLabels[i] == 0):
        if (probs[i][0] < 0.5):           
            falsePos += 1
        else:
            trueNeg += 1 
    if (testLabels[i] == 1):
        if (probs[i][0] > 0.5):
            falseNeg += 1
        else:
            truePos += 1

positive_recall = truePos/ (truePos + falseNeg)
positive_precision = truePos/ (truePos + falsePos)
negative_recall = trueNeg/ (trueNeg + falsePos)
negative_precision = trueNeg/ (trueNeg + falseNeg)
accuracy = (truePos +trueNeg)/(truePos +trueNeg +falseNeg + falsePos)

print("SKLEARN NAIVE BAYES")
print("pos_recall = " + str(positive_recall))
print("pos_precision = " + str(positive_precision))
print("neg_recall = " + str(negative_recall))
print("neg_precision = " + str(negative_precision))
print("accuracy = " + str(accuracy))
print('\n')
print('\n')
print('---------------')



# SKLEARN LOGISTIC REGRESSION


newPosTraining = trainingPos
newNegTraining = trainingNeg




posTrainStrings = []
negTrainStrings = []
for review in trainingPos:
    new = ''
    tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    noPunct = tokenizer.tokenize( review )
    for word in noPunct:
#         if word.lower() not in defaultStopwords:    
        new += word.lower()
        new += ' ' 
    posTrainStrings.append(new)
    
for review in trainingNeg:
    new = ''
    tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    noPunct = tokenizer.tokenize( review )
    for word in noPunct:
#         if word.lower() not in defaultStopwords:    
        new += word.lower()
        new += ' ' 
    negTrainStrings.append(new)
        
labelPosDocs = [1 for i in posTrainStrings]
labelNegDocs = [0 for i in negTrainStrings]

# create one large list of the docs (order does not matter)
training = posTrainStrings + negTrainStrings

# create one large list of the labels (order should match the docs)
labels = labelPosDocs + labelNegDocs

cv = CountVectorizer()
cv.fit_transform(training)
counts = cv.transform(training)

posTestLabels = [1 for i in testingPos]
negTestLabels = [0 for i in testingNeg]

testLabels = posTestLabels + negTestLabels

combinedTests = testingPos + testingNeg
 



testCounts = cv.transform(combinedTests)

scikit_log_reg = LogisticRegression(verbose=1,solver='liblinear',random_state=0, C=5, penalty='l2',max_iter=5000)
modelLR = scikit_log_reg.fit(counts, labels)
probs = modelLR.predict_proba(testCounts)

truePos = falsePos = trueNeg = falseNeg = 0
for i in range(len(probs)):

    if (testLabels[i] == 0):
        if (probs[i][0] < 0.5):           
            falsePos += 1
        else:
            trueNeg += 1 
    if (testLabels[i] == 1):
        if (probs[i][0] > 0.5):
            falseNeg += 1
        else:
            truePos += 1

positive_recall = truePos/ (truePos + falseNeg)
positive_precision = truePos/ (truePos + falsePos)
negative_recall = trueNeg/ (trueNeg + falsePos)
negative_precision = trueNeg/ (trueNeg + falseNeg)
accuracy = (truePos +trueNeg)/(truePos +trueNeg +falseNeg + falsePos)

print()
print("SKLEARN LOGISTIC REGRESSION")
print("pos_recall = " + str(positive_recall))
print("pos_precision = " + str(positive_precision))
print("neg_recall = " + str(negative_recall))
print("neg_precision = " + str(negative_precision))
print("accuracy = " + str(accuracy))
print('\n')
print('\n')
print('---------------')


















            
