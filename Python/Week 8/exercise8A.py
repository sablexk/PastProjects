# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:14:11 2020

@author: sstan
"""


import math
import nltk
from nltk.tokenize import RegexpTokenizer

def zValue (w, x, b):
    sum = 0
    i = 0
    for a in w:
        sum = sum + (w[i] * x[i])
        i = i + 1
    z = sum + b
    return z

def sigmoid(z):
    sig = 1 / (1 + math.exp(-1 * z))
    return sig

posLexicon = []
negLexicon = []

posWords = set()
negWords = set()

b = 0
w = [1, -2, -0.01]

posFP = open("hu_liu_positiveLexicon.txt", 'r')
negFP = open("hu_liu_negativeLexicon.txt", 'r') 
    
for line in posFP:
    aStr = line.replace('\n', '')
    posWords.add(aStr)
print("len(posWords)= " + str(len(posWords)))
    
for line in negFP:
   aStr = line.replace('\n', '')
   negWords.add(aStr)
print("len(negWords)= " + str(len(negWords)))

for e in posLexicon:
    posWords.add(e)
    
for e in negLexicon:
    negWords.add(e)



fullTestString = 'the movie was horrible,  I hated it!'
#fullTestString = 'It was a movie'
#fullTestString = 'it had a wonderful plot'
#fullTestString = 'the movie was wonderful, I loved it!  non-linear plot, great acting, enthralling.'
test = nltk.word_tokenize(fullTestString)

print('test = ' + str(test))
fv = [0,0,0]
for word in test:
    if word in posWords:
        fv[0] += 1
        print(word + " in posWords")
    if word in negWords:
        fv[1] += 1
        print(word + " in negWords")
fv[2] = len(fullTestString)

print("fv = " + str(fv))

w = [1, -2, -0.01]
b = 0;

z = zValue(fv, w, b)
print('z = ' + str(z))

y = sigmoid(z)
print('y = ' + str(y))

if (y > 0.5):
    print("positive")
else:
    print("negative")


