import os
import json

from .LetterFreq import LetterFreq
from .tools import weightedChoice

# Name generator class
# Loads database, create FreqLetter for all the ngrams ([2-N])
# Generates random names based on ngrams


class NameGenerator:

    # Constructor name generator
    def __init__(self, database, selectedNgram):
        self.database = database
        self.selectedNgram = selectedNgram

        self.databasePath = "data/" + self.database
        self.generatedPath = self.databasePath + "/generated/"
        self.generatedBaseName = self.generatedPath + self.database

    # Initialize the databse
    def init(self):
        # If the database does not exists, then the database will be created
        if not os.path.exists(os.path.dirname(self.generatedPath)):
            print("Database not found: The database will be created")
            print("Learning...")
            self.createDatabase()
            return

        # Generate database path
        fn = self.generatedBaseName + ".json"

        # Open first file (with N-GRAM)
        if os.path.isfile(fn):
            with open(fn, "r") as file:
                jsonMap = json.load(file)
                # ngram value is the data from the file
                # can be different than the selectedNgram
                self.ngram = jsonMap["ngram"]
        else:
            raise Exception("Loading: Database file not found")

        # Select N-GRAM is the min between
        # N-GRAM from the database and the selected one
        self.freqHolders = []
        selectedNgram = min(self.ngram, self.selectedNgram)

        # Load freq files
        self.loadFreqFiles(2, selectedNgram)

        # If the selected N-GRAM is higher than N-GRAM from the database
        # Then create all missing data
        self.createDatabase(True)

    def loadFreqFiles(self, beg, end):
        for i in range(beg, end):
            # Add a new frequence holder
            self.freqHolders.append(LetterFreq(i))

            # Generate the name
            ngram = str(self.freqHolders[-1].ngram)
            name = self.generatedBaseName + "_freq_" + ngram + ".json"

            # Load frequence file
            self.freqHolders[-1].loadFromFile(name)

    # Get selected N-GRAM
    def getSelectedNgram(self):
        return self.selectedNgram

    # Reload database
    def reload(self, selectedNgram):
        self.selectedNgram = selectedNgram
        self.createDatabase(True)

    # Create new database
    def createDatabase(self, relearn=False):

        # Check if is an update or creation
        if not relearn:
            # If is creation then all data are created
            beg = 2
            end = self.selectedNgram + 1
            self.freqHolders = []
        else:
            loadedFreqSize = len(self.freqHolders)
            if self.selectedNgram > self.ngram:
                # If is relearn then only new data are created
                beg = self.ngram
                end = self.selectedNgram + 1
            elif loadedFreqSize < self.selectedNgram - 2:
                # Just load not loaded files
                self.loadFreqFiles(loadedFreqSize, self.selectedNgram)
                return
            else:
                # Nothing to do because the selected N-GRAM is lower
                # than the max value from the database
                return

        # Generates all the previous N-GRAM for starting letters
        if end > 2:
            for i in range(beg, end):
                self.freqHolders.append(LetterFreq(i))

        # Open raw data
        fn = self.databasePath + "/data.dat"
        with open(fn, "r") as file:
            for line in file.readlines():
                # Extract name
                data = line[:-1]

                # Add name to all FreqLetters [2-N]
                for i in range(beg, end):
                    if len(data)+2 >= i:
                        self.freqHolders[i-2].addToCount(data)

        # Compute probabilities
        for i in range(beg, end):
            self.freqHolders[i-2].computeProbability()

        # Save data if is needed
        self.saveToFile()

        # The value of N-GRAM in the file is the selected value
        self.ngram = self.selectedNgram

    # Save NameGenerator data to json file
    def saveToFile(self):
        fn = self.generatedBaseName + ".json"
        jsonMap = {}

        jsonMap["ngram"] = self.selectedNgram

        if not os.path.exists(os.path.dirname(fn)):
            os.makedirs(os.path.dirname(fn))

        with open(fn, "w") as file:
            file.write(json.dumps(jsonMap))

        for freq in self.freqHolders:
            path = self.generatedBaseName + \
                "_freq_" + str(freq.ngram) + ".json"
            if not os.path.isfile(path):
                freq.saveToFile(path)

    # Generate a name
    def generate(self):
        # Pick The first letter randomly
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
            if len(word) < 100000:
                length = self.selectedNgram - 3
                nl = self.freqHolders[length].getNewLetter(word)
            else:
                nl = "!"
            word = word + nl

            if nl == "!":
                stillSomeLetters = False

        return word
