# leaving this one here to try the hill-climbing approach
import sys
import os
import time
import multiprocessing
import threading
import string
import re

key = {} #mapping dictionary from cypher to actual letters

english_freq = {"a" : 8.05, "b" : 1.62, "c" : 3.20, "d" : 3.65, "e" : 12.31, "f" : 2.28, "g" : 1.61, "h" : 5.14, "i" : 7.18, "j" : 0.10, "k" : 0.52, "l" : 4.03, "m" : 2.25, "n" : 7.19, "o" : 7.94, "p" : 2.29, "q" : 0.20, "r" : 6.03, "s" : 6.59, "t" : 9.59, "u" : 3.10, "v" : 0.93, "w" : 2.03, "x" : 0.20, "y" : 1.88, "z" : 0.09}

cypher_freq = {}

common_two_letters = ["of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if", "me", "my", "up", "an", "go", "no", "us", "am"]

common_three_letters = ["the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "had", "her", "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"]

common_four_letters = ["that", "with", "have", "this", "will", "your", "from", "they", "know", "want", "been", "good", "much", "some", "time"]

common_bigrams = ["th","he","in","er","an","re","ed","on","es","st","en","at","to","nt","ha"]

common_trigrams = ["the","ing","and","her","ere","ent","tha","nth","was","eth","for"]

common_quadgrams = {"TION" :  0.31,        "OTHE" :  0.16,        "THEM" :  0.12,
"NTHE" :  0.27,        "TTHE" :  0.16,        "RTHE" :  0.12,
"THER" :  0.24,        "DTHE" :  0.15,        "THEP" :  0.11,
"THAT" :  0.21,        "INGT" :  0.15,        "FROM" :  0.10,
"OFTH" :  0.19,        "ETHE" :  0.15,        "THIS" :  0.10,
"FTHE" :  0.19,        "SAND" :  0.14,        "TING" :  0.10,
"THES" :  0.18,        "STHE" :  0.14,        "THEI" :  0.10,
"WITH" :  0.18,        "HERE" :  0.13,        "NGTH" :  0.10,
"INTH" :  0.17,        "THEC" :  0.13,        "IONS" :  0.10,
"ATIO" :  0.17,        "MENT" :  0.12,        "ANDT" :  0.10}

def input_formatter():
    sentences = []
    with open(file, "r") as f:
        for line in f:          #splitting input up by sentences.
            sentences += line.strip().split(".")
    for i in range(len(sentences)):     #removing whitespace at the beginning of sentences.
        sentences[i] = sentences[i].translate(str.maketrans('', '', string.punctuation)).strip()
    return sentences

def get_n_grams(text, n, size=0): # takes text, find ngrams of size n, and outputs a freq. table of the ngram and also list of n_grams to the size provided
    total = 0
    n_grams = {}
    for sentence in text:
        words = sentence.split()
        for word in words:
            word = word.lower()
            i = 0
            while i + n <= len(word):
                if word[i:i+n] not in n_grams:
                    n_grams[word[i:i+n]] = 0
                n_grams[word[i:i+n]] += 1
                total += 1
                i+=1

    for k in n_grams:
        n_grams[k] = float("{:.2f}".format((n_grams[k]/total) * 100))   # converting totals to percentages

    if size > 0:
        return (n_grams,(sorted(n_grams, key=n_grams.get, reverse=True)[:size]))
    else:
        return n_grams

def find_len_n_words(text, n):
    a = []
    for sentence in text:
        words = sentence.split()
        if n > 1:
            for word in words:
                word = word.lower()
                if len(word) == n:
                    a.append(word)
        else:
            if words:
                if len(words[0]) == 1:  # if the first word of the sentence has len 1...
                    a.append(words[0].lower())  # add it to the array in it's lower form to avoid false positive for "I"
                for word in words[1:]:
                    if len(word) == n:
                        a.append(word)
    return a

def find_ai(len1, unigram_freqs):
    len1_d = {}
    len1_set = list(set(len1))
    n_unique_chars = len(len1_set)

    if n_unique_chars == 1:
        if len1_set[0].isupper():
            key["i"] = len1_set[0]
        else:
            key["a"] = len1_set[0]
        del unigram_freqs[len1_set[0]]
    elif n_unique_chars == 2:
        if len1_set[0].isupper():
            key["i"] = len1_set[0]
            key["a"] = len1_set[1]
        elif len1_set[1].isupper():
            key["i"] = len1_set[1]
            key["a"] = len1_set[0]
        else:
            for c in len1:
                if c not in len1_d:
                    len1_d[c] = 0
                len1_d[c] += 1
            key["a"] = max(len1_d, key=len1_d.get)
            key["i"] = min(len1_d, key=len1_d.get)
        del unigram_freqs[len1_set[0]]
        del unigram_freqs[len1_set[1]]
    elif n_unique_chars == 3:
        for item in len1_set:
            if item.isupper():
                key["i"] = item.lower()
                del unigram_freqs[item.lower()]
                break
        for item in len1_set:
            if item.lower() != key["i"]:
                key["a"] = item.lower()
                del unigram_freqs[item]
                break
    return unigram_freqs

def find_closest(c_freq):
    # finds english letter with closest freq to cypher letter.
    closest = ""
    min_diff = 100
    for k, v in english_freq.items():
        diff = abs(c_freq - v)
        if diff < min_diff:
            min_diff = diff
            closest = k
    return closest

def main():
    text = input_formatter() # formats the text into sentences
    unigram_freqs = get_n_grams(text, 1)
    key["e"] = max(unigram_freqs, key=unigram_freqs.get) # e is the letter with the highest freq
    del unigram_freqs[max(unigram_freqs, key=unigram_freqs.get)]

    #bigram_freqs, bigrams = get_n_grams(text, 2, 15)
    #trigram_freqs, trigrams = get_n_grams(text, 3, 11)
    #quadgram_freqs, quadgrams = get_n_grams(text, 4, 11)

    len1 = find_len_n_words(text, 1)
    len2 = find_len_n_words(text, 2)
    len3 = find_len_n_words(text, 3)
    len4 = find_len_n_words(text, 4)

    unigram_freqs = find_ai(len1, unigram_freqs) #tries to place A and I into the keys

    #[k, [key matches], v , [value matches]]
    possibilities = []
    for k, v in key.items():
        key_matches = set()
        value_matches = set()
        for word in common_two_letters:
            if k in word:
                key_matches.add(word.replace(k, ""))
        for word in len2:
            if v in word:
                value_matches.add(word.replace(v,""))
        if len(key_matches) > 0 and len(value_matches) > 0:
            possibilities.append([list(value_matches), list(key_matches)])

    print(sorted(unigram_freqs,key=unigram_freqs.get,reverse=True))

    for a in possibilities:
        for letter in a[0]:
            letter_freq = unigram_freqs[letter]
            print(f"{letter} freq =",letter_freq)
            closest_match = ""
            best_freq_diff = 100
            for k,v in english_freq.items():
                if k not in key.keys():
                    if abs(letter_freq - v) < best_freq_diff:
                        print(k, " freq =", v)
                        closest_match = k
                        best_freq_diff = abs(letter_freq - v)
            print(best_freq_diff, letter, closest_match)
            key[closest_match] = letter

    for k, v in key.items():
        print(f"{k} : {v}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            file = sys.argv[1]
            main()
        else:
            print("invalid file path provided")
    else:
        print("no file path arg provided")