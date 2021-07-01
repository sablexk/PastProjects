# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:46:20 2020

@author: sstan
"""


f = open("tale_chapter1.txt", 'r', encoding="utf8")

story = f.read()

#print(story)

import re
novel = story.split()
novel = " ".join(novel)
novella = re.split('([\.])',novel)
# for w in novella:
#     print(w.lstrip(), end='\n')
    

for i in range(0,len(novella)):
    if ( (i%2) == 0):
        rewrite = novella[i].lstrip().rstrip() # in rstrip in case an trailing whitespace
        if (i < (len(novella) - 1) ):  # don't exceed list boundary
            rewrite = rewrite + novella[i+1]
            print(rewrite)
         