import sys
import os

results = []

for dirpath, dirnames, files in os.walk('results'):
    print(f'Found directory: {dirpath}')
    for file_name in files:
        results.append(file_name)

for fn in results:
    total = 0
    with open("results/" + fn,"r") as f:
        for line in f:
            total += float(line.strip())
        with open("all_averages.txt", "a") as f:
            f.write(f"{fn} average = {(total/20):.2f} seconds\n")

