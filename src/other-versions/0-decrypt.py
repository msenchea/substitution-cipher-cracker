#This was a letter by letter oriented approach. It was a failure.

import sys
import os
import time
import multiprocessing
import threading
import string


def main():
    english_letter_frequency = "etaoinsrhldcumfpgwybvkxjqz"
    cypher_text_frequency = ""
    freq_dict = {}
    with open(file,"r") as f:
        for line in f:
            for letter in line:
                if letter not in string.punctuation and letter != " ":
                    letter = letter.lower()
                    if letter not in freq_dict:
                        freq_dict[letter] = 0
                    freq_dict[letter] += 1

    for k in sorted(freq_dict, key=freq_dict.get, reverse=True):
        cypher_text_frequency += k
    for i in range(26-len(cypher_text_frequency)):
        cypher_text_frequency += string.punctuation[i]  #temporarily placing random punctuation until I figure it out
    print(english_letter_frequency)
    print(cypher_text_frequency)
    mapping = {}
    for i in range(len(english_letter_frequency)):
        mapping[cypher_text_frequency[i]] = english_letter_frequency[i]

    cracked = ""
    with open(file, "r") as f:
        for line in f:
            for c in line:
                if c.lower() in mapping:
                    cracked += mapping[c.lower()]
                else:
                    cracked += c
    print(cracked)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            file = sys.argv[1]
            main()
        else:
            print("invalid file path provided")
    else:
        print("no file path arg provided")