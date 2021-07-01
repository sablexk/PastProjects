# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:44:08 2020

@author: sstan
"""


from random import random

# this function has no bearing an reality, its only purpos
# is to take in postive/negative test documents and return "positive" or "negative"
# so you can calculate the various recall, precision, and accuracy measures.
def runModel(s):
	rNum = random()
	if ('neg' in s):
		if (rNum < 0.3):
			return('positive')
		else:
			return('negative')
	if ('pos' in s):
		if (rNum < 0.4):
			return('negative')
		else:
			return('positive')

# Gold Labels
posTests = [
'posTest0',
'posTest1',
'posTest2',
'posTest3',
'posTest4',
'posTest5',
'posTest6',
'posTest7',
'posTest8',
'posTest9'
]

negTests = [
'negTest0',
'negTest1',
'negTest2',
'negTest3',
'negTest4',
'negTest5',
'negTest6',
'negTest7',
'negTest8',
'negTest9'
]



print("Running positive tests")
truePos_count = 0
falseNeg_count = 0
for s in posTests:
    result = runModel(s)
    print(result)
	# do calculation here to keep track of truePostives and falseNegatives
    if result == "positive":
        truePos_count += 1
    else:
        falseNeg_count += 1

print("Running negative tests")
trueNeg_count = 0
falsePos_count = 0
for s in negTests:
    result = runModel(s)
    print(result)
	# do calculation here to keep track of trueNegatives and falsePositives
    if result == "negative":
        trueNeg_count += 1
    else:
        falsePos_count += 1
# write code to calculate the postiveRecall, postivePrecision, negativeRecall, negativePrecision, and accuracy
# It should calculate these measure for the 20 tests (not once per test, but all of the measure for the 20 tests as a group)


# calculate 
pos_recall = (truePos_count)/(truePos_count + falseNeg_count)
pos_precision = (truePos_count)/(truePos_count + falsePos_count)
neg_recall = (trueNeg_count)/(trueNeg_count + falsePos_count)
neg_precision = (trueNeg_count)/(trueNeg_count + falseNeg_count)
accuracy = (truePos_count + trueNeg_count)/(trueNeg_count + falsePos_count + truePos_count + falseNeg_count) 



print("\n")
print("positive recall: " + str(pos_recall))
print("positive precision: " + str(pos_precision))
print("negative recall: " + str(neg_recall))
print("negative precision: " + str(neg_precision))
print("accuracy: " + str(accuracy))
   