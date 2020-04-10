import sys
import os
import time
import multiprocessing
import threading
import string

def main():
    freq_dict = {}
    with open(file,"r") as f:
        for line in f:
            for letter in line:
                if letter not in string.punctuation and letter != " ":
                    letter = letter.lower()
                    if letter not in freq_dict:
                        freq_dict[letter] = 0
                    freq_dict[letter] += 1

    for k, v in freq_dict.items():
        print(f"{k}:{v}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            file = sys.argv[1]
            main()
        else:
            print("invalid file path provided")
    else:
        print("no file path arg provided")