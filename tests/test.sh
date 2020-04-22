#!/usr/bin/env bash

for i in `seq 1 20`
do
    python3 single_test.py alice-in-wonderland-cipher.txt
    python3 multi_test.py alice-in-wonderland-cipher.txt
    python3 single_test.py russell-cipher.txt
    python3 multi_test.py russell-cipher.txt
    python3 single_test.py os-sub-cipher.txt
    python3 multi_test.py os-sub-cipher.txt
    python3 single_test.py two-cities-cipher.txt
    python3 multi_test.py two-cities-cipher.txt

done