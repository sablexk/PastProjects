# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:26:21 2020

@author: sstan
"""


# Khai Lai, Cooper Huston, Sam Stanton
# Exercise 4

import nltk

# download necessary component of the package
nltk.download("stopwords")
nltk.download("punkt")

from nltk.text import Text
from urllib import request
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.probability import FreqDist


url = "http://www.gutenberg.org/cache/epub/1228/pg1228.txt"
response_origin = request.urlopen(url)
raw_origin = response_origin.read().decode("utf8")


sherlock_url = (
    "https://www.gutenberg.org/files/1661/1661-0.txt"  # Adventures of Sherlock Holmes
)
response_sherlock = request.urlopen(sherlock_url)
raw_sherlock = response_sherlock.read().decode("utf8")

# remove punctuation first
tokenizer = RegexpTokenizer(r"\w+")
no_punct_origin = tokenizer.tokenize(raw_origin)
no_punct_sherlock = tokenizer.tokenize(raw_sherlock)

# convert no-punction version into NTLK text
origin_text = nltk.Text(no_punct_origin)
sherlock_text = nltk.Text(no_punct_sherlock)

# most common yet unuseful words in the english language
default_stopwords = stopwords.words("english")

# create frequency distributions of th useful words in each text
origin_fdist = FreqDist()
sherlock_fdist = FreqDist()

for word in origin_text.tokens:
    if word not in default_stopwords:
        origin_fdist[word.lower()] += 1

for word in sherlock_text.tokens:
    if word not in default_stopwords:
        sherlock_fdist[word.lower()] += 1

# print("Origin FreqDist: {}".format(str(origin_fdist)))
# print("*" * 100)
# print("Sherlock FreqDist: {}".format(str(sherlock_fdist)))

O = set([word[0] for word in origin_fdist.most_common(100)])
B = set([word[0] for word in sherlock_fdist.most_common(100)])

print("*" * 100)
print("Origin most common 100: {}".format(O))
print("-" * 100)
print("Sherlock most common 100: {}".format(B))

# find set difference between the two books
BminusO = B.difference(O)
OminusB = O.difference(B)
print("*" * 100)
print("B - O = {}".format(BminusO))
print("-" * 100)
print("O - B = {}".format(OminusB))

# find average word length in Origin
character_count_origin = 0
for word in origin_text.tokens:
    character_count_origin += len(word)

avg_word_length_origin = character_count_origin / len(origin_text.tokens)

# find average word length in Sherlock
character_count_origin = 0
for word in sherlock_text.tokens:
    character_count_origin += len(word)

avg_word_length_sherlock = character_count_origin / len(sherlock_text.tokens)
print("*" * 100)
print("average word length in origin: {}".format(avg_word_length_origin))
print("average word length in sherlock: {}".format(avg_word_length_sherlock))

# finding average sentence length for origin
origin_sentences = sent_tokenize(raw_origin)
total_length = 0
for sentence in origin_sentences:
    total_length += len(sentence)
avg_sentence_length_origin = total_length / len(origin_sentences)

# finding average sentence length for sherlock
sherlock_sentences = sent_tokenize(raw_sherlock)
total_length = 0
for sentence in sherlock_sentences:
    total_length += len(sentence)
avg_sentence_length_sherlock = total_length / len(sherlock_sentences)
print("*" * 100)
print("average sentence length in origin: {}".format(avg_sentence_length_origin))
print("average sentence length in sherlock: {}".format(avg_sentence_length_sherlock))
