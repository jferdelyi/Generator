import json

from .LetterFreq import LetterFreq
from .tools import weightedChoice

# Name generator class
# Loads database, create FreqLetter for all the ngrams ([2-N])
# Generates random names based on ngrams


class NameGen:
    # Constructor name generator
    def __init__(self, ngrams):
        self.ngram = ngrams

    # Initialize NameGenerator using database
    # Optionnal argument, read function:
    # 	if set, use the function to extract town name
    #	eg: file format is "name;otherInfo;otherInfo;...\n"
    #		readFun = lambda line: line.split(";")[0]
    def init(self, database, readFun=None):
        # Generates all the previous n-grams for starting letters
        if self.ngram > 2:
            self.freqHolders = []
            for i in range(2, self.ngram+1):
                self.freqHolders.append(LetterFreq(i))

        # Loads database
        with open(database, "r") as file:
            for line in file.readlines():
                # Exctract name
                name = ""
                if readFun != None:
                    name = readFun(line)
                else:
                    name = line[:-1]  # For ville.out

                # Add name to all FreqLetters [2-N]
                for i in range(2, self.ngram+1):
                    if len(name)+2 >= i:
                        self.freqHolders[i-2].addToCount(name)

        for frq in self.freqHolders:
            frq.computeProbability()

    # Generate a name
    def generate(self):
        # Pick The first letter randomly
        firstLetters = None

        firstLetters = weightedChoice(self.freqHolders[0].freqMap["$"])

        # Take the (ngram-2) next letter given the n-grams
        firstLetters = "$" + firstLetters
        for j in range(3, self.ngram):
            nStartLetter = self.freqHolders[j-2].getNewLetter(firstLetters)
            firstLetters = firstLetters + nStartLetter

            if nStartLetter == "!":
                return firstLetters

        # Beginning of word is set, lets continue !
        word = firstLetters
        stillSomeLetters = True
        while stillSomeLetters:
            # Security
            if len(word) < 50:
                nl = self.freqHolders[-1].getNewLetter(word)
            else:
                nl = "!"
            word = word + nl

            if nl == "!":
                stillSomeLetters = False

        return word

    # Save NameGenerator data to json file
    def saveToFile(self, fn):
        jsonMap = {}

        jsonMap["ngram"] = self.ngram

        with open(fn, "w") as file:
            file.write(json.dumps(jsonMap))

        for freq in self.freqHolders:
            freq.saveToFile(fn + "_freq_"+str(freq.ngram))

    # load NameGenerator data from json file
    def loadFromFile(self, fn):
        jsonMap = {}
        with open(fn, "r") as file:
            jsonMap = json.load(file)

        self.ngram = jsonMap["ngram"]
        self.freqHolders = []

        for i in range(2, self.ngram):
            self.freqHolders.append(LetterFreq(i))
            self.freqHolders[-1].loadFromFile(fn +
                                              "_freq_"+str(self.freqHolders[-1].ngram))
