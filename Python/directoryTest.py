# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:00:38 2020

@author: sstan
"""


#aStr = input("Enter a string: ")
#print ("You typed: " + aStr)


f = open("testfile.txt", 'r')

bigString = f.read()

print (bigString)