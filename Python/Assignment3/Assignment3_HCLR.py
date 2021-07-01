# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:24:54 2020

@author: sstan
"""


#HAND CODED LOGISTIC REGRESSION
#Lifted from Week 10 code

import nltk
from queue import Queue
from math import exp, log
from random import random, randint
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
defaultStopwords = stopwords.words('english')   # can get other languages
debug = False

# from sklearn.model_selection import train_test_split


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



#---------------  end of doOneIteration() function 


# create set of wordsPositive by reading in from file
wordsPositive = set()
fpp = open("positive-words.txt",mode='r',encoding="ISO-8859-1")
for line in fpp:
	aStr = line.replace('\n','')
	wordsPositive.add(aStr)
# print("len(wordsPositive) = " + str(len(wordsPositive)))

# create set of wordsNegative by reading in from file
wordsNegative = set()
fpn = open("negative-words.txt",mode='r',encoding="ISO-8859-1")
for line in fpn:
	aStr = line.replace('\n','')
	line.replace('\n','')
	wordsNegative.add(aStr)
# print("len(wordsNegative) = " + str(len(wordsNegative)))


#  assume four input files exist:   
#	posTrain.txt	- the postive training set
#	negTrain.txt	- the negative training set
#	posTest.txt	- the positive test set
#	negTest.txt	- the negative test set


	
verbose = False
positiveDocs = []
negativeDocs = []

# read in, tokenize, and remove stop words for posTrain.txt => file of postive training documents
# fpPosTrain = open('posTrain.txt', 'r') 
# for line in fpPosTrain:
# 	positiveDocs.append(line)
# # Now remove all stopwords
# posTrainStrings = []
# for s in positiveDocs:
# 	new = ''
# 	tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
# 	noPunct = tokenizer.tokenize( s )
# 	for word in noPunct:
# 		if word.lower() not in defaultStopwords:    
# 			new += word.lower()
# 			new += ' '
# 	posTrainStrings.append(new)
# if verbose:
# 	print("\n\nposTrainStrings = ")
# 	print(posTrainStrings)
# 	print("\n\n")

# # read in, tokenize, and remove stop words for negTrain.txt => file of negative documents 
# fpNegTrain = open('negTrain.txt', 'r') 
# for row in fpNegTrain:
# 	negativeDocs.append(row)
# # Now remove all stopwords
# negTrainStrings = []
# for s in negativeDocs:
# 	new = ''
# 	tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
# 	noPunct = tokenizer.tokenize( s )
# 	for word in noPunct:
# 		if word.lower() not in defaultStopwords:    
# 			new += word.lower()
# 			new += ' '
# 	negTrainStrings.append(new)
# if verbose:
# 	print("\n\nnegTrainStrings = ")
# 	print(negTrainStrings)
# 	print("\n\n")

X = posTrainStrings + negTrainStrings
Y_pos = [1 for doc in posTrainStrings]
Y_neg = [0 for doc in negTrainStrings]
Y = Y_pos + Y_neg
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.1, random_state=1)












'''
# create the test string/tokens
posTrainStrings = [
'the movie was wonderful, i loved it! great plot, nice acting, enthralling.',
'best move ever!  I love katherine hepburn, she is so witty and tough.',
'bogie is the best, amazing intensity, the master of macho, good and fair.',
'The most enjoyable and wonderful 3 hours I have spent in years.'
]
negTrainStrings = [
'dreadful, dull and plodding plot, i left after 20 minutes.',
'snore! the most boring three hours of movie torture ever made. The acting was so bad it made me cringe.',
'horrendously bad movie.  do not go, you will regret it! This movie is worse than dirty grandpa, horrible, horrible, horrible!',
'bad acting, horrible plot, lame visual effects.  utter was of time and money.',
]
'''


#------- function to take in a document, represented as a string, and return a feature vector
def createFeatureVector(s):
	fv = [0,0,0]
	tokens = nltk.word_tokenize(s)
	for word in tokens:
		if word in wordsPositive:
			fv[0] += 1
		if word in wordsNegative:
			fv[1] += 2
	fv[2] = 0.0001 * len(s)
	return(fv)



# Now create a feature vector for each document, it is these feature vectors we will use going
# forward, not the documents themselves


    
fv_train = []
for document in X_train:
    fv = createFeatureVector(document)
    fv_train.append(fv)


print("feature vectors:")
for v in fv_train:
	print(v)


# GLOBAL global vars defined here
# learning rate - too large and overshoot, too small and many iterations needed...
globalETA = 0.01
w = [0, 0, 0]   # the three weight values that correspond to the feature vector and used in dot-product
b = 0  # bias adjustment
theta = [0,0,0,0]  # w and b combined, algorithm in book uses "theta" so we will follow
grad = [1,1,1,1]   # gradient



# a function to return the average abs(gradient) value - devieation from a gradient of zero
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


#============= beginning of stochastic gradient descent loop
iterationCount = 0 
print("About to start gradient descent, w & b set to 0, eta = " + str(globalETA) )

# Keep doing iterations until some stopping condition, like LCE (of a subset of documents)  <= 0.001
# NOTE: another logical stopping condition would be when the gradient drops below a threshold
loopReport = True
# while (iterationCount < 200000) and (avgGrad() > 0.0001) :
while (iterationCount < 200000):
	iterationCount += 1
	# pick a document feature vector at random
	# if ((iterationCount % 2) == 0):   # alternate neg/pos set, not sure which of alternating/random is better
	# randomly choose from X_train
	rNum = randint(0,len(fv_train)-1)
	x = fv_train[rNum]
	y = Y_train[rNum]  # tagged positive, so y = 1
	
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

	if (loopReport) and ((iterationCount % 200) == 0):
		print('finished iteration ' + str(iterationCount))
		print('y = ' + str(y) + ', x = ' + str(x))
		print('theta = ' + str(theta))
		print('avgGrad() = ' + str(avgGrad()) + ', grad = ' + str(grad))
		print('LCE = ' + str(LCE))

print("\n\nAt end of stochastic gradient descent:")
print('iterationCount = ' + str(iterationCount))
print('avgGrad() = ' + str( avgGrad()))
print('w = ' + str(w))
print('b = ' + str(b))

#============= end of stochastic gradient descent loop


'''
print("positive training documents (feature vectors) classifed as:")
for fv in posFeatureVectors:
	print(fv)
	y = 1
	z = zValue(fv,w,b)
	yPrime = sigma(z)
	print('yPrime = ' + str(yPrime))
	if (yPrime > 0.5):
		print("classified as positive")
	else:
		print("classified as negative")
print("negative training documents (feature vectors) classifed as:")
for fv in negFeatureVectors:
	print(fv)
	y = 0
	z = zValue(fv,w,b)
	yPrime = sigma(z)
	print('yPrime = ' + str(yPrime))
	if (yPrime > 0.5):
		print("classified as positive")
	else:
		print("classified as negative")
	
print("\n\nNow run on some test documents")
'''


'''
negTestStrings = [
'the original was dumb, this is beyond dumb, totally inane',
'one of the worst movies ever, total garbage.  boring! I hated it!',
'boring, spectacularly bad, inane, horrible!'
]
posTestStrings = [
'totally awesome, one of the best movies ever!',
'loved it, fun, and engrossing. great plot',
'fabulous! Beautifully done, a tour de force'

]
'''





truePos = trueNeg = falsePos = falseNeg = 0

print("\n\nClassifying positive test documents:")

for i in range(len(X_test)):
    
    fv = createFeatureVector(X_test[i]) 
    print(fv)
    z = zValue(fv,w,b)
    yPrime = sigma(z)
    true_y = Y_test[i]
	# print('yPrime = ' + str(yPrime))
    if (yPrime > 0.5):
        # classify as positive       
        if (true_y == 1):
            truePos += 1
        else:
            falsePos += 1
    else:
        # classify as negative
        if (true_y == 1):
            falseNeg += 1
        else:
            trueNeg += 1




print("theta = " + str(theta))
print("iterationCount = " + str(iterationCount))
print("avgGrad = " + str( avgGrad() ))
print("truePos = " + str(truePos))
print("trueNeg = " + str(trueNeg))
print("falsePos = " + str(falsePos))
print("falseNeg = " + str(falseNeg))
print("accuracy = " + str( (truePos+trueNeg) / (truePos+trueNeg+falsePos+falseNeg)))