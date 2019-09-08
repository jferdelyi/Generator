#!/usr/bin/env python3

import sys
import random
import time

from classes.SingletonNameGenerator import SingletonNameGenerator

random.seed()
hasParam = len(sys.argv) > 0

if not hasParam or not "-load" in sys.argv or not "-ngram" in sys.argv:
    print("Error, need number of N-GRAM and database name")
    print("-load <database>")
    print("-ngram <ngram>")
    exit(1)

if "-load" in sys.argv:
    i = sys.argv.index("-load")
    if len(sys.argv) > i + 1:
        database = sys.argv[i + 1]
        print("Set database: " + database)
    else:
        print("Warning, need filename to save")
        exit(1)

if "-ngram" in sys.argv:
    i = sys.argv.index("-ngram")
    if len(sys.argv) > i + 1:
        ngram = int(sys.argv[i + 1])
        print("Set N-GRAM: " + str(ngram))
    else:
        print("Error, need number of ngram")
        exit(1)

t0 = time.time()
print("Load learning...")
SingletonNameGenerator.init(database, ngram)
print("Done in {0}s".format(round(time.time() - t0, 3)))

running = True
print("Press 'enter' to generate new word or 'q' to quit")
while running:
    data = input()
    if data == 'q':
        print("Quit...")
        running = False
    else:
        print(SingletonNameGenerator.generate())
