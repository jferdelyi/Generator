import json

from .tools import weightedChoice

# Compute  and holds probability for n-gram
# Add words to LetterFreq to build and count n-grams
# Compute probability of all added words
# Use it as a random letter generator (given the ngram-1 previous letter)


class LetterFreq:
    def __init__(self, ngram):
        self.ngram = ngram
        self.ngramCount = 0
        self.valueMap = {}
        self.freqMap = {}

    # Count ngrams
    def addToCount(self, word):
        if self.ngram != 1:
            # $ is starting ! is ending
            word = "$" + word.lower() + "!"

        for i in range(len(word)-(self.ngram-1)):
            # Getting the current n-gram
            current = word[i:i+self.ngram]

            # Access the value map
            currMap = self.valueMap
            currFreqMap = self.freqMap
            for c in current[:-1]:
                # Create freq if not existing
                if c not in currMap:
                    currMap[c] = {}
                    currFreqMap[c] = {}

                currMap = currMap[c]
                currFreqMap = currFreqMap[c]

            # Create counter if not exist
            if current[-1] not in currMap:
                currMap[current[-1]] = 0
                currFreqMap[current[-1]] = 0.0

            # Update count
            currMap[current[-1]] = currMap[current[-1]]+1

        self.ngramCount = self.ngramCount+len(word)-self.ngram

    # Compute ngram probability (recursively)
    def computeProbability(self):
        self._recurseComputeProb(self.freqMap, self.valueMap)

    # Recursive N-gram calculation
    def _recurseComputeProb(self, freqObj, countObj):
        kList = list(freqObj.keys())
        if len(kList) > 0:
            firstKey = kList[0]
            if isinstance(freqObj[firstKey], dict):
                for k in freqObj:
                    self._recurseComputeProb(freqObj[k], countObj[k])
            else:
                for k in freqObj:
                    freqObj[k] = countObj[k]/float(self.ngramCount)

    # Pick a random ngram
    def getNewLetter(self, currentWord):
        if len(currentWord) > self.ngram-1:
            current = currentWord[-(self.ngram-1):]
        else:
            current = currentWord

        currentFreq = self.freqMap
        for c in current:
            currentFreq = currentFreq[c]

        return weightedChoice(currentFreq)

    # Save Frequency data to json file
    def saveToFile(self, fn):
        jsonMap = {}

        jsonMap["ngram"] = self.ngram
        jsonMap["ngramCount"] = self.ngramCount
        jsonMap["valueMap"] = self.valueMap
        jsonMap["freqMap"] = self.freqMap

        with open(fn, "w") as file:
            file.write(json.dumps(jsonMap))

    # Load Frequency data to json file
    def loadFromFile(self, fn):
        jsonMap = {}
        with open(fn, "r") as file:
            jsonMap = json.load(file)

        self.ngram = jsonMap["ngram"]
        self.ngramCount = jsonMap["ngramCount"]
        self.valueMap = jsonMap["valueMap"]
        self.freqMap = jsonMap["freqMap"]
