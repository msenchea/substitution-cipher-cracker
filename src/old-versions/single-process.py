import sys
import os
import time
import multiprocessing
import threading
import string
from random import randint, shuffle
from math import log10
from copy import deepcopy
import queue

def load_scores_file():
    quadgram_scores = {}
    with open("quadgram_scores.txt", "r") as f:
        for line in f:
            k, v = line.strip().split()
            quadgram_scores[k] = float(v)
    return quadgram_scores

def get_score(text, quadgram_scores):
    ''' compute the score of text using quadgram scores dictionary '''
    total_score = 0
    min_score = -11.625737060717677
    for i in range(len(text)-4): # this for loop gives a score to each and every quadgram in the cypher-text being passed.
        if text[i:i+4] in quadgram_scores:
            total_score += quadgram_scores[text[i:i+4]]
        else:
            total_score += min_score # if the quadgram doesn't exist in the dict, give the quadgram the minimum score.
    return total_score

def input_formatter(inputfile):
    ''' formats the input, removes punctuation, spaces and makes everything uppercase '''
    text = ""
    with open(inputfile, "r") as f:
        for line in f:
            text += "".join(list(filter(lambda x: x.isalpha(), line))).upper() # filters out all non alphabetic characters
    return text

def create_freq_table(text):
    letter_freqs = {}
    for letter in text:  
        if letter not in letter_freqs:
            letter_freqs[letter] = 0
        letter_freqs[letter] += 1
    return letter_freqs

def create_freq_key(freq_table):
    ''' creates key based on most common letter frequencies in the english language '''
    origin_key = "".join(sorted(freq_table, key=freq_table.get, reverse=True))
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

def text_decrypter(text, key):
    ''' translates text using the given key and returns the translated text '''
    cypher_dict = {}
    decyphered_text = ""
    for k, v in zip(key, string.ascii_uppercase):
        cypher_dict[k] = v
    for letter in text:
        decyphered_text += cypher_dict[letter]
    return decyphered_text

def codebreaker(quadgram_scores, text, key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    ''' finds key using quadgram frequencies and randomly swapping key values '''
    best_key = key
    best_score = get_score(text_decrypter(text, best_key), quadgram_scores) # setting a baseline score using given key

    count = 0
    while count < 1000: # if the count reaches 1000 random keys without finding a new best, the key should be found.
        key = list(best_key[:])
        a = randint(0,25)
        b = randint(0,25)
        key[a], key[b] = key[b], key[a]
        key_score = get_score(text_decrypter(text, "".join(key)), quadgram_scores)

        if key_score > best_score:
            best_score = key_score
            best_key = key
            count = 0
        else:
            count += 1

        count += 1

    return(best_key, best_score)


def generate_output_files(inputfile, key):
    mapping = {}
    for k, v in zip(key, string.ascii_uppercase):
        mapping[k] = v

    plaintext = ""
    with open(inputfile, "r") as f:
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
    out = inputfile.strip().rsplit(".",1)[0]

    with open(f"{out}-decrypted.txt", "w") as outputfile:
        for line in plaintext:
            outputfile.write(line)
    with open(f"{out}-key.txt", "w") as keyfile:
        for k,v in mapping.items():
            keyfile.write(f"{v} = {k}\n")

def main(inputfile):
    start_time = time.time()
    quadgram_scores = load_scores_file()
    text = input_formatter(inputfile)
    freq_table = create_freq_table(text)
    freq_key = create_freq_key(freq_table)
    alphabet = list(string.ascii_uppercase)

    best_key, best_score = codebreaker(quadgram_scores, text, freq_key)

    for _ in range(2):
        key, score = codebreaker(quadgram_scores, text, freq_key)
        if score > best_score:
            best_score = score
            best_key = key

    for _ in range(3):
        key, score = codebreaker(quadgram_scores, text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if score > best_score:
            best_score = score
            best_key = key
        shuffle(alphabet)
        key, score = codebreaker(quadgram_scores, text, "".join(alphabet))
        if score > best_score:
            best_score = score
            best_key = key

    print(best_key)
    generate_output_files(inputfile, best_key)


    print(f"time elapsed = {time.time() - start_time:.2f} seconds") # calculate and print time elapsed

if __name__ == "__main__":
    #main("os-sub-cipher.txt")
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            inputfile = sys.argv[1]
            main(inputfile)
        else:
            print("invalid file path arg provided")
    else:
        print("no file path arg provided")