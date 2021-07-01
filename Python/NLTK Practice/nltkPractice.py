# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 08:32:02 2020

@author: sstan
"""
# Testing NLTK - a simple program to make sure it is working
# To run this you need to have installed NLTK
# Make sure you can run this before class, i.e your nltk works.
# If you are using anaconda, this should be as easy as running the command:
#     conda install nltk
# If that did not work, or you are using something other than spyder/anacona, google is your friend!


from nltk.book import text2, sent2



# show the title info on the imported texts
# texts()

print("\nText2:")
print( text2 )

# show first 40 words of text2
print("\ntext2[:40]:\n")
print( text2[:40] )

# show first sentence of text 2
print("\nFirst sentence of text2, i.e. print(sent2):\n")
print ( sent2 )

# length of text2
print("\nprint(len(text2)):\n")
print ( len(text2) )

ind1 = text2.index('Dashwood')
print("\nprint(ind1): \n")
print ( ind1 )

print("\nprint(text2[ind1:ind1+10]): \n")
print ( text2[ind1:ind1+10] )

# last 70 words of text2
print("\nSpoiler!  Last 70 words, i.e. print(text2[-70:]):\n")
print ( text2[-70:] )
print("\nAs a string, last 70 words:")
aStr = " ".join(text2[-70:])
print("\n" + aStr)

