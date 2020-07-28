import sys
import os
import time
import multiprocessing
import threading
import string

potential_letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

letter_count = 0

english_freq_table = {
    "a" : 8.05,
    "b" : 1.62,
    "c" : 3.20,
    "d" : 3.65,
    "e" : 12.31,
    "f" : 2.28,
    "g" : 1.61,
    "h" : 5.14,
    "i" : 7.18,
    "j" : 0.10,
    "k" : 0.52,
    "l" : 4.03,
    "m" : 2.25,
    "n" : 7.19,
    "o" : 7.94,
    "p" : 2.29,
    "q" : 0.20,
    "r" : 6.03,
    "s" : 6.59,
    "t" : 9.59,
    "u" : 3.10,
    "v" : 0.93,
    "w" : 2.03,
    "x" : 0.20,
    "y" : 1.88,
    "z" : 0.09
}

def input_formatter(file):
    Sentences = []
    with open(file, "r") as f:
        for line in f:
            Sentences += line.strip().split(".")
    print(Sentences)

def main():
    global letter_count
    english_letter_frequency = "etaoinsrhldcumfpgwybvkxjqz"
    cypher_text_frequency = ""
    cypher_letters = []
    count_dict = {}
    with open(file,"r") as f:
        for line in f:
            line = line.strip().split()
            for word in line:
                for letter in word:
                    if letter not in string.punctuation and letter != " ":
                        letter_count += 1
                        letter = letter.lower()
                        if letter not in count_dict:
                            cypher_letters.append(letter)
                            count_dict[letter] = 0
                        count_dict[letter] += 1

    freq_dict = {}
    for c in count_dict:
        freq_dict[c] = float("{:.2f}".format((count_dict[c]/letter_count) * 100))
    print(sorted(freq_dict, key=freq_dict.get, reverse=True))

    #for k in sorted(count_dict, key=count_dict.get, reverse=True): #creates a string of frequency of letters from the cypher.
    #    cypher_text_frequency += k

    mapping = {"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":"","i":"","j":"","k":"","l":"","m":"","n":"","o":"","p":"","q":"","r":"","s":"","t":"","u":"","v":"","w":"","x":"","y":"","z":""} #mapping dictionary from cypher to actual letters


    cracked = ""
    with open(file, "r") as f:
        for line in f:
            for c in line:
                if c.lower() in mapping:
                    cracked += mapping[c.lower()]
                else:
                    cracked += c
    print(cracked)
    print("".join(sorted(english_freq_table, key=english_freq_table.get, reverse=True)).upper())


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            file = sys.argv[1]
            main()
        else:
            print("invalid file path provided")
    else:
        print("no file path arg provided")