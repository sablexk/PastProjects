# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:10:18 2020

@author: sstan
"""



import nltk
from nltk.corpus import wordnet
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
defaultStopwords = stopwords.words('english')


from random import randint

def get_random_ints(num_ints, max_num):
    setOfRandomInts = set()
    while len(setOfRandomInts) < num_ints:
        rNum = randint(0, max_num)
        setOfRandomInts.add(rNum)
    return(setOfRandomInts)


# helper function to count how many times a word, w,  occurs in a list, aList
def count_W_inList(w, aList):
	count = 0
	for w2 in aList:
		if w2 == w:
			count += 1
	return(count)

# positive training documents
AboutEquity = ["I would agree that poorly designed training sets can be a problems. They introduce unintended bias that affects the outcomes of the algorithms. If the algorithm is only specialized in a certain type of data, it will fail to accurate work with new types of data introduced.",

    "I agree because if we train these models to be racist or something like that then over time, they will always be racist or biased in some sort of manor. As we start to rely on these machines more and more for things, this can pose huge issues and flaws in our logic.",

    "Yes; the better you are able to represent the population your data draws from, the better prepared your program will be to accurately assess what it comes across. This makes common sense, and yet it it so easy to ignore if we are thinking outside of our normal CS bubble. Many of us don't think about or want to think about social impacts our programs can make, especially at the early stages of a project.",

    "Yes because poorly designed training sets can lead to bias where it can output inaccurate data. This can misrepresent what the program initially design for. ",

    "Yes! Person who collected the training set probably has some inherent subconscious bias and didn't think to include enough data that correctly represent the diverse range of possible data classes! ",

    "Yes they limit the potential of other people and exclude others from equal opportunities. Plus they are biased in nature, by whoever the creators are.",

    "I absolutely agree with the speaker that poorly designed training sets can be a problem, because they can perpetuate the systems of discrimination in our society. There have been literacy tests, the Grandfather Clause, gerrymandering, and voter ID laws. Society should be moving away from discriminatory practices, not inadvertently or consciously continuing them. ",

    "absolutely; such training sets spread the implicit bias that was created within the sets. Many people also put a significant amount of trust into artificial intelligence/other algorithms and if those are unreliable then people relying on them is incredibly dangerous",

    "Yes- especially with her example with the facial recognization software not being able to recognize her face due to her color is definitely an issue, especially when the software is meant for all users of all 'spectrum'. Poorly designed training sets mean that the designers are not considering all angles for their software, limiting its potential",

    "I definitely agree. Not only can poor training sets lead to bias, but can give noisy and uninteresting results",

    "Yes! Clearly poor training sets can reinforce inequity.",

    "Yes! I am terrified to see ML/AI may actually perpetuate and strengthen systemic racism instead of helping to dismantle racism.",

    "I agree. Not only poorly designed training sets create a technical problem, but the societal implications need to be considered.",

    "I agree. If training poorly designed sets result in algorithmic bias than clearly there is a social justice issue here!",

    "Yes, I agree. Clearly one can build bias into an algorithm.  We need to work towards removing bias, not codifying it in future software!"

    ]

 

 

AboutTechnology = [

    "I agree, if the training set is to narrow then the probability space will be too small resulting in a narrow model that fails to have good precision.",

    "I agree in this situation because training sets are intended to give the people using code a somewhat rounded experience of software so they can expand what it can do. If training sets are poorly designed, then it makes testing software more difficult, and then it can take away from time spent actually working with the software if you have to teach it a new set of information or to use new data. ",

    "Poorly designed training sets can definitely be a huge problem. If a training set is poorly designed, then it will not properly train people and create a chain affect of problems, which can create life threatening mistakes.",

    "I agree because a poorly designed training set will not adequately capture the all the types of queries that will be run and hence the model will fail to be a good classifier.",

    "I agree. If a data set is not sufficiently varied then the model will fail to make accurate predictions.",

    "I agree, the training set needs to have sufficient coverage and size to enable high quality classification.",

    "I agree, a training set needs to cover a sufficiently large space of words to allow for meaninful classification.",

    "I agree.  More and more machine learning is going to be used in the future, so it is important that students understand the importance of crafting robust training sets.",

    "I agree because if the sets don't encompass a wide variety, then there will be subsets that are left out when its time for the software to actually run.",

    "I agree. Poorly designed training sets could result in statisitical correlations that result in poor classification."

    ]
Accuracy_i = []

for i in range (0, 10):
    print("\n\nTest Number " + str(i))
    
    trainingEq = []
    trainingTech = []
    testingEq = []
    testingTech = []
    
    eqInt = []
    eqInt = get_random_ints(3, 14)
    # print(eqInt)
    
    
    
    for i in range(0, 15):
        if i in eqInt:
            testingEq.append(AboutEquity[i])
        else:
            trainingEq.append(AboutEquity[i])
       
    
    techInt = []
    techInt = get_random_ints(2, 9)
    # print(techInt)
    
   
    for i in range(0, 10):
        if i in techInt:
            testingTech.append(AboutTechnology[i])
        else:
            trainingTech.append(AboutTechnology[i])   

    
    # there are 2 postive and 3 negative in the training
    total = len(trainingEq) + len(trainingTech)
    ProbEq = len(trainingEq) / total
    ProbTech  = len(trainingTech) / total
    
    newAboutEquity = []
    newAboutTechnology = []
    
    for s in trainingEq:
    
        new = ''
    
        tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
    
        noPunct = tokenizer.tokenize( s )
    
        for word in noPunct:
    
            if word.lower() not in defaultStopwords:
    
                new += word.lower()
    
                new += ' '
    
        newAboutEquity.append(new)
    
    
    for s in trainingTech:
    
        new = ''
        tokenizer = RegexpTokenizer(r'\w+')   # use NOT alphanumeric as token separator
        noPunct = tokenizer.tokenize( s )
    
        for word in noPunct:
            if word.lower() not in defaultStopwords:
                new += word.lower()
                new += ' '
    
        newAboutTechnology.append(new)
        
    
    def get_word_count(word, dictionary):
        if word in dictionary:
            return dictionary[word]
        else:
            return 0
    
    V = set()
    bagEq = {}   # bagEq: words in "positive" class
    for s in newAboutEquity:
    	ts = nltk.word_tokenize(s)
    	for w in ts:
    		if w in bagEq:
    			bagEq[w] +=1
    		else:
    			bagEq[w] =1
    		V.add(w)
    
    bagTech = {}   # bagTech: words in "negative" class
    for s in newAboutTechnology:
    	ts = nltk.word_tokenize(s)
    	for w in ts:
    		if w in bagTech:
    			bagTech[w] +=1
    		else:
    			bagTech[w] =1
    		V.add(w)
            
    true_pos = 0
    false_neg = 0
    for fullTestString in testingEq:
        print("\n\nTest document = " + fullTestString)
        fullTestList = nltk.word_tokenize(fullTestString)
        test = [ w for w in fullTestList if w in V]     
        
        likelihoodW_eq = {} 
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagEq) + 1)
    
        for w in test:
         	likelihoodW_eq[w] =  (get_word_count(w, bagEq) + 1) / denominator
     
        likelihoodW_tech = {} # dictionary of probabilities for negative class
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagTech) + 1)
    
        for w in test:
         	likelihoodW_tech[w] =  (get_word_count(w, bagTech) + 1) / denominator
    
        finalProbTech = ProbTech 
        for w in test:
         	finalProbTech *=  likelihoodW_tech[w]
    
        finalProbEq = ProbEq 
        for w in test:
         	finalProbEq *=  likelihoodW_eq[w]
      
        if (finalProbEq > finalProbTech):
            true_pos += 1
            print("\nModel predicts the test query belongs in the EQUITY class")
        else:
            false_neg += 1
            print("\nModel predicts the test query belongs in the TECHNICAL class")
    
    true_neg =0
    false_pos = 0        
    for fullTestString in testingTech:
        print("\n\nTest document = " + fullTestString)
        fullTestList = nltk.word_tokenize(fullTestString)
        test = [ w for w in fullTestList if w in V]     
        
        likelihoodW_eq = {} 
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagEq) + 1)
    
        for w in test:
         	likelihoodW_eq[w] =  (get_word_count(w, bagEq) + 1) / denominator
     
        likelihoodW_tech = {} # dictionary of probabilities for negative class
        
        denominator = 0
        for w in V:
         	denominator += (get_word_count(w, bagTech) + 1)
    
        for w in test:
         	likelihoodW_tech[w] =  (get_word_count(w, bagTech) + 1) / denominator
    
        finalProbTech = ProbTech 
        for w in test:
         	finalProbTech *=  likelihoodW_tech[w]
    
        finalProbEq = ProbEq 
        for w in test:
         	finalProbEq *=  likelihoodW_eq[w]
      
        if (finalProbEq > finalProbTech):
            false_pos += 1
            print("\nModel predicts the test query belongs in the EQUITY class")
        else:
            true_neg += 1
            print("\nModel predicts the test query belongs in the TECHNICAL class")
    
    print("\ntrue_pos = " + str(true_pos))
    print("\nfalse_neg = " + str(false_neg))
    print("\ntrue_neg = " + str(true_neg))
    print("\nfalse_pos = " + str(false_pos))
    
    Accuracy_i.append((true_pos + true_neg)/(true_pos + true_neg + false_pos + false_neg))
i = 0
sum_accuracies =0
print("\n\nResults")
for accuracy in Accuracy_i:
    print("\nAccuracy_" + str(i) + " " + str(Accuracy_i[i])) 
    sum_accuracies += Accuracy_i[i]
    i += 1
print("Average Accuracy = " + str(sum_accuracies/10))
    
    
    
    
    