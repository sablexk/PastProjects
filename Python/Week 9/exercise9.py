# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:05:46 2020

@author: sstan
"""


'''
nltk7d1.py

This example shows how to do gradient descent using the magnitude of the gradient as the stopping condition.


It assumes the same simple feature vector mapping fucntion as before:

# fv[0] = number of words in "good lexicon"
# fv[1] = number of words in "bad lexicon"
# fv[2] = length of review  # hypothesis: the longer the review the more negative...

We start with w = [0,0,0] and b = 0


In each iteration of the descent algorithm (Figure 5.5) we:
  - select a training document from our set of training documents
  - calculate the gradient, 
  - theta = theta - (eta * gradient)
  - set w & b to theta to get new w & b
  - calculate the new cross entropy loss value

The stopping condition is when either the gradient becomes sufficiently close to zero, 
or the number of iterations surpasses a threshold
'''

import nltk
from queue import Queue
from math import exp, log
from random import random, randint, randrange
debug = False


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
fpp = open("hu_liu_positiveLexicon.txt",mode='r',encoding="ISO-8859-1")
for line in fpp:
	aStr = line.replace('\n','')
	wordsPositive.add(aStr)
# print("len(wordsPositive) = " + str(len(wordsPositive)))

# create set of wordsNegative by reading in from file
wordsNegative = set()
fpn = open("hu_liu_negativeLexicon.txt",mode='r',encoding="ISO-8859-1")
for line in fpn:
	aStr = line.replace('\n','')
	line.replace('\n','')
	wordsNegative.add(aStr)
# print("len(wordsNegative) = " + str(len(wordsNegative)))


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


#------- function to take in a document, represented as a string, and return a feature vector
def createFeatureVector(s):
	fv = [0,0,0]
	tokens = nltk.word_tokenize(s)
	for word in tokens:
		if word in wordsPositive:
			fv[0] += 1
		if word in wordsNegative:
			fv[1] += 2
	fv[2] = len(s)
	return(fv)

#----------- Randomly select 2 from posTrain and 2 from negTrain


rand = randint(0, 3)
randPosTrain = ['', '']
copyPos = posTrainStrings.copy()
for i in range(2):
    randPosTrain[i] = copyPos[rand]
    copyPos.remove(copyPos[rand])
    rand = randint(0, len(copyPos))
    
    
randNegTrain = ['','']
rand = randint(0, 3)
copyNeg = negTrainStrings.copy()

for i in range(2):
    randNegTrain[i] = copyNeg[rand]
    copyNeg.remove(copyNeg[rand])
    rand = randint(0, len(copyNeg))
    
    
    
    
# Now create a feature vector for each document, it is these feature vectors we will use going
# forward, not the documents themselves

posFeatureVectors = []
for s in posTrainStrings:
	fv = createFeatureVector(s)
	posFeatureVectors.append(fv)

negFeatureVectors = []
for s in negTrainStrings:
	fv = createFeatureVector(s)
	negFeatureVectors.append(fv)


print("feature vectors for positive training set are:")
for v in posFeatureVectors:
	print(v)
print("feature vectors for negative training set are:")
for v in negFeatureVectors:
	print(v)

# GLOBAL global vars defined here
# learning rate - too large and overshoot, too small and many iterations needed...
globalETA = 0.0001
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
loopReport = False
while (iterationCount < 200000) and (avgGrad() > 0.001) :
	iterationCount += 1
	# pick a document feature vector at random
	# if ((iterationCount % 2) == 0):   # alternate neg/pos set, not sure which of alternating/random is better
	if (random() < 0.5):  # randomly choose from pos set
		rNum = randint(0,len(posFeatureVectors)-1)
		x = posFeatureVectors[rNum]
		y = 1  # tagged positive, so y = 1
	else: 	# randomly choose from pos set
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

	if (loopReport):
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


posTestVectors = []
for s in posTestStrings:
	fv = createFeatureVector(s)
	posTestVectors.append(fv)

negTestVectors = []
for s in negTestStrings:
	fv = createFeatureVector(s)
	negTestVectors.append(fv)


print("\n\nClassifying positive test documents:")
print(posTestVectors)
for fv in posTestVectors:
	print(fv)
	z = zValue(fv,w,b)
	yPrime = sigma(z)
	print('yPrime = ' + str(yPrime))
	if (yPrime > 0.5):
		print("classified as positive")
	else:
		print("classified as negative")

print("\n\nClassifying negative test documents:")
print(negTestVectors)
for fv in negTestVectors:
	print(fv)
	z = zValue(fv,w,b)
	yPrime = sigma(z)
	print('yPrime = ' + str(yPrime))
	if (yPrime > 0.5):
		print("classified as positive")
	else:
		print("classified as negative")

