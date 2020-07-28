import sys
import os
import time
import multiprocessing
import threading
import string
from random import randint, shuffle
from math import log10

ALPHABET = list(string.ascii_uppercase)
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
        self.N = sum(self.ngrams.values()) # N = total of all values frequency values
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

class Decypher:
    def __init__(self, inputfile):
        self.inputfile = inputfile
        if len(self.inputfile.split("/")) > 1:
            self.filepath = "/".join(inputfile.strip().split("/")[:-1]) + "/"
        else:
            self.filepath = ""
        self.filename = inputfile.strip().split("/")[-1].split(".")[0]
        self.text = self.input_formatter()
        self.quadgrams = ngram_score("quadgrams.txt")   # loading up quadgrams score dictionary
        self.freq_table = self.create_freq_table()
        self.freq_key = self.create_freq_key()
        self.global_best_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.global_best_score = -99e99

    def text_decrypter(self, key):
        ''' translates text using the given key and returns the translated text '''
        cypher_dict = {}
        decyphered_text = ""
        for k, v in zip(key, string.ascii_uppercase):
            cypher_dict[k] = v
        for letter in self.text:
            decyphered_text += cypher_dict[letter]
        return decyphered_text

    def input_formatter(self):
        ''' formats the input, removes punctuation, spaces and makes everything uppercase '''
        text = ""
        with open(self.inputfile, "r") as f:
            for line in f:
                text += "".join(list(filter(lambda x: x.isalpha(), line))).upper() # filters out all non alphabetic characters
        return text

    def create_freq_table(self):
        letter_freqs = {}
        for letter in self.text:  # can be done with np at the same time as above? would it even be necessary?
            if letter not in letter_freqs:
                letter_freqs[letter] = 0
            letter_freqs[letter] += 1
        return letter_freqs

    def create_freq_key(self):
        ''' creates key based on most common letter frequencies in the english language '''
        origin_key = "".join(sorted(self.freq_table, key=self.freq_table.get, reverse=True))
        english_freq = "ETAONISRHLDCUPFMWYBGVKQXJZ"

        if len(origin_key) < 26: # if the ciphertext doesn't have all the letters in it, complete the key with the remaining letters
            origin_key += "".join(set(english_freq).difference(set(origin_key)))

        freq_key = ""
        temp = {}
        for k, v in zip(english_freq, origin_key):
            temp[k] = v
        for k in sorted(temp):
            freq_key += temp[k]
        return freq_key

    def codebreaker(self, key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        ''' finds key using quadgram frequencies and randomly swapping key values '''
        best_key = key
        best_score = self.quadgrams.score(self.text_decrypter(best_key)) # setting a baseline score using given key

        count = 0
        while count < 1000: # if the count reaches 1000 random keys without finding a new best, the key should be found.
            key = list(best_key[:])
            a = randint(0,25)
            b = randint(0,25)
            key[a], key[b] = key[b], key[a]
            key_score = self.quadgrams.score(self.text_decrypter("".join(key)))

            if key_score > best_score:
                best_score = key_score
                best_key = key
                count = 0
            else:
                count += 1

            count += 1

        if best_score > self.global_best_score:
            self.global_best_score = best_score
            self.global_best_key = best_key
        print(best_key)

    def generate_output_files(self):
        mapping = {}
        for k, v in zip(self.global_best_key, string.ascii_uppercase):
            mapping[k] = v

        plaintext = ""
        with open(self.inputfile, "r") as f:
            for line in f:
                for c in line:
                    if c.upper() in mapping:
                        letter = mapping[c.upper()]
                        if c.isupper():
                            plaintext += letter
                        else:
                            plaintext += letter.lower()
                    else:
                        plaintext += c

        print(plaintext)

        with open(f"{self.filepath}{self.filename}-decrypted.txt", "w") as outputfile:
            for line in plaintext:
                outputfile.write(line)
        with open(f"{self.filepath}{self.filename}-key.txt", "w") as keyfile:
            for k,v in mapping.items():
                keyfile.write(f"{v} = {k}\n")


def main(inputfile):
    start_time = time.time() # starting timer to time speed of program
    decrypter = Decypher(inputfile) # initialising class using input file supplied
    decrypter.codebreaker(decrypter.freq_key)
    decrypter.codebreaker()
    decrypter.codebreaker()
    decrypter.codebreaker(decrypter.freq_key)
    decrypter.codebreaker(decrypter.freq_key)
    decrypter.codebreaker(decrypter.freq_key)
    shuffle(ALPHABET)
    decrypter.codebreaker("".join(ALPHABET))
    shuffle(ALPHABET)
    decrypter.codebreaker("".join(ALPHABET))
    shuffle(ALPHABET)
    decrypter.codebreaker("".join(ALPHABET))
    shuffle(ALPHABET)
    decrypter.codebreaker("".join(ALPHABET))

    decrypter.generate_output_files()   # generate the output file and write to original file path
    print(f"time elapsed = {time.time() - start_time:.2f} seconds") # calculate and print time elapsed

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            inputfile = sys.argv[1]
            main(inputfile)
        else:
            print("invalid file path arg provided")
    else:
        print("no file path arg provided")