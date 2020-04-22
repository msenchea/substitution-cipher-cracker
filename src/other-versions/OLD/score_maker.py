import sys
import os
import time
import multiprocessing
import threading
import string
from random import randint, shuffle
from math import log10

class ngram_score(object):
    def __init__(self,ngramfile):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}    # dictionary which stores quadgrams and their scores.
        with open(ngramfile, "r") as f: # populate the dictionary using the quadgram file
            for line in f:
                key,count = line.strip().split(" ")
                self.ngrams[key] = int(count)
        self.L = len(key)   # L = length of ngrams supplied in the text file (in my case it will always be 4)
        self.N = sum(self.ngrams.values()) # N = total of all values frequency values
        #calculate log probabilities
        for key in list(self.ngrams.keys()):
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N) # changing all values to their log probabilites.
        self.floor = log10(0.01/self.N) # creating a very low score for ngrams which don't match ngrams any in the ngrams dictionary


quadgrams = ngram_score("quadgrams.txt")
print(quadgrams.floor)

with open("quadgram_scores.txt","w") as f:
    for k, v in quadgrams.ngrams.items():
        f.write(f"{k} {v}\n")