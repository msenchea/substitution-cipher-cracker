import sys
import os
import time
import multiprocessing
import threading
import string
from random import randint, shuffle
from math import log10

ALPHABET = list(string.ascii_uppercase)
# The cracking concept used in this code (scores) was found on http://practicalcryptography.com/media/cryptanalysis/.
# quagram_scores.txt was also generated from the above website's "quadgrams.txt" file.

class Decypher:
    def __init__(self, text, scores):
        #self.inputfile = inputfile
        #if len(self.inputfile.split("/")) > 1:
        #    self.filepath = "/".join(inputfile.strip().split("/")[:-1]) + "/"
        #else:
        #    self.filepath = ""
        #self.filename = inputfile.strip().split("/")[-1].split(".")[0]
        self.text = text
        self.min_score = -11.625737060717677
        self.quadgram_scores = scores   # loading up quadgrams score dictionary
        self.freq_table = self.create_freq_table()
        self.freq_key = self.create_freq_key()
        self.global_best_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.global_best_score = -99e99
        self.codebreaker()
        self.codebreaker()
        self.codebreaker()
        self.codebreaker()

    def load_scores_file(self):
        quadgram_scores = {}
        with open("quadgram_scores.txt", "r") as f:
            self.min_score = float(f.readline().strip())
            for line in f:
                k, v = line.strip().split()
                quadgram_scores[k] = float(v)
        return quadgram_scores

    def get_score(self,text):
        ''' compute the score of text '''
        total_score = 0
        for i in range(len(text)-4): # this for loop gives a score to each and every quadgram in the cypher-text being passed.
            if text[i:i+4] in self.quadgram_scores:
                total_score += self.quadgram_scores[text[i:i+4]]
            else:
                total_score += self.min_score # if the quadgram doesn't exist in the dict, give the quadgram the minimum score.
        return total_score

    def text_decrypter(self, key):
        ''' translates text using the given key and returns the translated text '''
        cypher_dict = {}
        decyphered_text = ""
        for k, v in zip(key, string.ascii_uppercase):
            cypher_dict[k] = v
        for letter in self.text:
            decyphered_text += cypher_dict[letter]
        return decyphered_text

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
        best_score = self.get_score(self.text_decrypter(best_key)) # setting a baseline score using given key

        count = 0
        while count < 1000: # if the count reaches 1000 random keys without finding a new best, the key should be found.
            key = list(best_key[:])
            a = randint(0,25)
            b = randint(0,25)
            key[a], key[b] = key[b], key[a]
            key_score = self.get_score(self.text_decrypter("".join(key)))

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

    def generate_output_files(self, inputfile):
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


def init_object(i, text, scores):
    obj = Decypher(text, scores)
    print(str(i) + " " + "".join(obj.global_best_key))

def load_scores_file():
    quadgram_scores = {}
    with open("quadgram_scores.txt", "r") as f:
        for line in f:
            k, v = line.strip().split()
            quadgram_scores[k] = float(v)
    return quadgram_scores

def input_formatter(inputfile):
    ''' formats the input, removes punctuation, spaces and makes everything uppercase '''
    text = ""
    with open(inputfile, "r") as f:
        for line in f:
            text += "".join(list(filter(lambda x: x.isalpha(), line))).upper() # filters out all non alphabetic characters
    return text


def main(inputfile):
    start_time = time.time() # starting timer to time speed of program
    quadgrams = load_scores_file()
    text = input_formatter(inputfile)
    PROCESS_COUNT = 3

    processes = []

    for i in range(PROCESS_COUNT):
        p = multiprocessing.Process(target=init_object(i, text, quadgrams))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    #decrypter.generate_output_files()   # generate the output file and write to original file path
    print(f"time elapsed = {time.time() - start_time:.2f} seconds") # calculate and print time elapsed

if __name__ == "__main__":
    main("os-sub-cipher.txt")
    #if len(sys.argv) == 2:
    #    if os.path.isfile(sys.argv[1]):
    #        inputfile = sys.argv[1]
    #        main(inputfile)
    #    else:
    #        print("invalid file path arg provided")
    #else:
    #    print("no file path arg provided")