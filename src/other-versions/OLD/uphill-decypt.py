import sys
import os
import time
import multiprocessing
import threading
import string
from random import randint
from math import log10

alphabet = string.ascii_uppercase

# The following class, ngram_score, was taken from http://practicalcryptography.com/media/cryptanalysis/files/ngram_score_1.py. I do not own any of the code. I have slightly modified it to my needs.
# I have added my own comments to it to show that I understand it.

class ngram_score(object):
    def __init__(self,ngramfile):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}    # dictionary which stores quadgrams and their scores.
        with open(ngramfile, "r") as f: # populate the dictionary using the quadgram file
            for line in f:
                key,count = line.strip().split(" ")
                self.ngrams[key] = int(count)
        self.L = len(key)   # L = length of ngrams supplied in the text file (in my case it will always be 4)
        self.N = sum(self.ngrams.values()) # N = total of all values
        #calculate log probabilities
        for key in list(self.ngrams.keys()):
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N) # changing all values to their log probabilites.
        self.floor = log10(0.01/self.N) # creating a very low score for ngrams which don't match ngrams any in the ngrams dictionary

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):     # this for loop gives a score to each and every quadgram in the cypher-text being passed.
            if text[i:i+self.L] in self.ngrams:
                score += ngrams(text[i:i+self.L])
            else:
                score += self.floor     # if the quadgram doesn't exist, give the quadgram the minimum score.
        return score

def text_decrypter(key, text):
    ''' translates text using the given key and returns the translated text '''
    cypher_dict = {}
    decyphered = ""
    for k, v in zip(key, alphabet):
        cypher_dict[k] = v
    for letter in text:
        decyphered += cypher_dict[letter]
    return decyphered

def input_formatter():
    ''' formats the input, removes punctuation, spaces and makes everything uppercase '''
    text = ""
    with open(inputfile, "r") as f:
        for line in f:          #splitting input up by sentences.
            text += "".join(list(filter(lambda x: x.isalpha(), line))).upper()
            #text += line.translate(str.maketrans('', '', string.punctuation)).strip().replace(" ", "").strip().upper()
    return text

def create_freq_table(text):
    letter_freqs = {}
    for letter in text:  # can be done with np at the same time as above? would it even be necessary?
        if letter not in letter_freqs:
            letter_freqs[letter] = 0
        letter_freqs[letter] += 1
    return letter_freqs


def main(inputfile):
    start_time = time.time()
    text = input_formatter()
    quadgrams = ngram_score("quadgrams.txt") # can be done with mp?
    freq_table = create_freq_table(text)

    origin_key = "".join(sorted(freq_table, key=freq_table.get, reverse=True)) # creating first key based on letter frequency to try speed things up
    english_freq = "ETAONISRHLDCUPFMWYBGVKQXJZ"

    if len(origin_key) < 26: # if the ciphertext doesn't have all the letters in it, complete the key with the remaining letters
        origin_key += "".join(set(english_freq).difference(set(origin_key)))

    best_key = ""   # creating the first best key by putting the origin key in alphabetical order
    temp = {}
    for k, v in zip(english_freq, origin_key):
        temp[k] = v
    for k in sorted(temp):
        best_key += temp[k]

    best_score = quadgrams.score(text_decrypter(best_key, text))
    print(best_score)
    count = 0
    while count < 1000: # if the count reaches 1000 random keys without finding a new best, the key should be found.
        key = list(best_key[:])
        a = randint(0,25)
        b = randint(0,25)
        key[a], key[b] = key[b], key[a]
        key_score = quadgrams.score(text_decrypter("".join(key), text))

        if key_score > best_score:
            best_score = key_score
            best_key = key
            count = 0
        else:
            count += 1

        count += 1

    print(best_key)
    print(best_score)

    mapping = {}
    for k, v in zip(best_key, alphabet):
        mapping[k] = v

    cracked = ""
    with open(inputfile, "r") as f:
        for line in f:
            for c in line:
                if c.upper() in mapping:
                    letter = mapping[c.upper()]
                    if c.isupper():
                        cracked += letter
                    else:
                        cracked += letter.lower()
                else:
                    cracked += c

    print(best_key)

    #with open(f"{filepath}{filename}-decrypted.txt", "w") as outputfile:
    #    for line in cracked:
    #        outputfile.write(line)
    #with open(f"{filepath}{filename}-key.txt", "w") as keyfile:
    #    for k,v in mapping.items():
    #        keyfile.write(f"{v} = {k}\n")

    print(f"time elapsed = {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            inputfile = sys.argv[1]
            filepath = "/".join(sys.argv[1].strip().split("/")[:-1]) + "/"
            filename = sys.argv[1].strip().split("/")[-1].split(".")[0]

            processes = []
            for i in range(10):
                p = multiprocessing.Process(target=main(inputfile))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
        else:
            print("invalid file path arg provided")
    else:
        print("no file path arg provided")