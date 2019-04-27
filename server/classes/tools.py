import random

# Make a random choice with weighted values
# input: {"key1": 1, "key2": 4, "key3": 2}
# output: (example) "key 1"
def weightedChoice(values):    
    total = sum(w for c, w in values.items())
    r = random.uniform(0, total)
    upto = 0
    for c, w in values.items():
        if upto + w >= r:
            return c
        upto += w

    # Should never go there
    return values[list(values.keys())[0]]
