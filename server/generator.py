#!/usr/bin/env python3

import random
import sys

from classes.SingletonNameGenerator import SingletonNameGenerator

random.seed()
hasParam = len(sys.argv) > 0

if not hasParam:
    print("Error, need number of ngram and database name")
    exit(1)

if "-g" in sys.argv:
    i = sys.argv.index("-ngram")
    if len(sys.argv) > i + 1:
        ngram = int(sys.argv[i + 1])
        print("Set ngram: " + str(ngram))
    else:
        print("Error, need number of ngram")
        exit(1)

if "-n" in sys.argv:
    i = sys.argv.index("-load")
    if len(sys.argv) > i + 1:
        database = sys.argv[i + 1]
        print("Set database: " + database)
    else:
        print("Warning, need filename to save")
        exit(1)

print("Learning.")
SingletonNameGenerator.init(database, ngram)
print("Saving.")
SingletonNameGenerator.generator.saveToFile(database)
