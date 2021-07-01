# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:24:22 2020

@author: sstan
"""


import nltk
from math import exp, log


def zValue(fv,w,b):
	if (len(fv) != len(w)):
		print("ERROR, length mismatch, exiting...")
		exit()
	z = 0
	for i in range(0,len(fv)):
		z += fv[i] * w[i]
	z += b
	return(z)

def sigma(z):
	return( 1.0 / (1 + exp(-z)))

posWords = set()
posFP = open("hu_liu_positiveLexicon.txt",mode='r',encoding="ISO-8859-1")
for line in posFP:
	aStr = line.replace('\n','')
	posWords.add(aStr)


negWords = set()
negFP = open("hu_liu_negativeLexicon.txt",mode='r',encoding="ISO-8859-1")
for line in negFP:
	aStr = line.replace('\n','')
	line.replace('\n','')
	negWords.add(aStr)





# fullTestString = 'the movie was horrible,  I hated it!'
# fullTestString = 'It was a movie'
# fullTestString = 'it had a wonderful plot'
fullTestString = 'the movie was wonderful, I loved it!  non-linear plot, great acting, enthralling.'
test = nltk.word_tokenize(fullTestString)


print('test = ' + str(test))
fv = [0,0,0]
for word in test:
	if word in posWords:
		fv[0] += 1
	if word in negWords:
		fv[1] += 1
fv[2] = len(fullTestString)

print("fv = " + str(fv))

w = [1, -2, -0.01]   
b = 0

print('w = ' + str(w))

z = zValue(fv,w,b)
print('z = ' + str(z))

y = sigma(z)
print('y = ' + str(y))

if (y > 0.5):
	print("positive")
else:
	print("negative")

print("\n")

w = [1, -2, -0.01]   
b = 0 
x = fv


y = 1 
# y = 0
print("zValue(w,x,b) = " + str(zValue(w,x,b)))
LCE_1 = -1 * ( y * log(sigma(zValue(w,x,b))) + (1-y) * log( 1 - sigma(zValue(w,x,b))))
print('\nw = ' + str(w))
print("LCE_1 = " + str(LCE_1))


w = [1, -2, -0.001]
b = 0 
x = fv  # x is our feature vector
LCE_2 = -1 * ( y*log(sigma(zValue(w,x,b))) + (1-y)*log( 1 - sigma(zValue(w,x,b))))
print('\nw = ' + str(w))
print("LCE_2 = " + str(LCE_2))


w = [2, -2, -0.01]
b = 0 
x = fv  
LCE_3 = -1 * ( y*log(sigma(zValue(w,x,b))) + (1-y)*log( 1 - sigma(zValue(w,x,b))))
print('\nw = ' + str(w))
print("LCE_3 = " + str(LCE_3))


w = [2, -2, -0.001]
b = 0 
x = fv
LCE_4 = -1 * ( y*log(sigma(zValue(w,x,b))) + (1-y)*log( 1 - sigma(zValue(w,x,b))))
print('\nw = ' + str(w))
print("LCE_4 = " + str(LCE_4))