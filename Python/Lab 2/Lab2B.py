# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:29:50 2020

@author: sstan
"""


#f = open("dreamMLK.txt", 'r', encoding="utf8")

#story = f.read()

#print(story) ch Ch cH CH sh sH Sh SH [cCsS][Hh]

import re
with open("dreamMLK.txt",'r', encoding="utf8") as fp:
    line = fp.readline()
    count = 1
    while line:
        if (re.search('[cCsS][hH]',line)):  
            print(str(count) + ": " + line)
            splitLine = re.split(" ", line)
            
            print(re.findall(r'\b[cCsS][hH]\w+ | \s\b\w+[cCsS][hH]\w+', line.upper()))
            
        line = fp.readline()
        count = count + 1
        
        