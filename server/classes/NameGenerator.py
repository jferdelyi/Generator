import os
import json

from .LetterFreq import LetterFreq
from .tools import weightedChoice

# Name generator class
# Loads database, create FreqLetter for all the ngrams ([2-N])
# Generates random names based on ngrams


class NameGenerator:

    # Constructor name generator
    # if ngram is not -1 the value in the file is ignored
    def __init__(self, ngram):
        self.selectedNgram = ngram

    def reload(self, database, ngram):
        if self.ngram < ngram:
            print("Relearn is needed")
            self.createDatabase(database, ngram)

            self.selectedNgram = ngram
            self.saveToFile(database)
        else:
            self.selectedNgram = ngram

    # Create new database
    def createDatabase(self, database, newNgram=-1):
        if newNgram == -1:
            beg = 2
            end = self.selectedNgram + 1
            self.freqHolders = []
        else:
            beg = self.ngram
            end = newNgram + 1
        self.ngram = newNgram

        # Generates all the previous n-grams for starting letters
        if end > 2:
            for i in range(beg, end):
                self.freqHolders.append(LetterFreq(i))

        # Open raw data
        fn = "data/" + database + "/data.dat"
        with open(fn, "r") as file:
            for line in file.readlines():
                # Extract name
                data = line[:-1]

                # Add name to all FreqLetters [2-N]
                for i in range(2, end):
                    if len(data)+2 >= i:
                        self.freqHolders[i-2].addToCount(data)

        for frq in self.freqHolders:
            frq.computeProbability()

    # Save NameGenerator data to json file
    def saveToFile(self, database):
        baseName = "data/" + database + "/generated/" + database
        fn = baseName + ".json"
        jsonMap = {}

        jsonMap["ngram"] = self.selectedNgram

        if not os.path.exists(os.path.dirname(fn)):
            try:
                os.makedirs(os.path.dirname(fn))
            except OSError as exc:  # Guard against race condition
                raise exc

        with open(fn, "w") as file:
            file.write(json.dumps(jsonMap))

        for freq in self.freqHolders:
            path = baseName + "_freq_" + str(freq.ngram) + ".json"
            if not os.path.isfile(path):
                freq.saveToFile(path)

    # load NameGenerator data from json file
    def loadFromFile(self, database):
        baseName = "data/" + database + "/generated/" + database
        fn = baseName + ".json"
        jsonMap = {}
        with open(fn, "r") as file:
            jsonMap = json.load(file)

        self.selectedNgram = jsonMap["ngram"]
        self.ngram = self.selectedNgram
        self.freqHolders = []

        for i in range(2, self.selectedNgram):
            self.freqHolders.append(LetterFreq(i))
            name = baseName + "_freq_" + \
                str(self.freqHolders[-1].ngram) + ".json"
            self.freqHolders[-1].loadFromFile(name)

        return self.selectedNgram

        # Generate a name
    def generate(self):
        # Pick The first letter randomly
        firstLetters = None

        firstLetters = weightedChoice(self.freqHolders[0].freqMap["$"])

        # Take the (ngram-2) next letter given the n-grams
        firstLetters = "$" + firstLetters
        for j in range(3, self.selectedNgram):
            nStartLetter = self.freqHolders[j-2].getNewLetter(firstLetters)
            firstLetters = firstLetters + nStartLetter

            if nStartLetter == "!":
                return firstLetters

        # Beginning of word is set, lets continue !
        word = firstLetters
        stillSomeLetters = True
        while stillSomeLetters:
            # Security
            if len(word) < 100:
                length = self.selectedNgram - 3

                nl = self.freqHolders[length].getNewLetter(word)
            else:
                nl = "!"
            word = word + nl

            if nl == "!":
                stillSomeLetters = False

        return word
