from .NameGen import NameGen

# Singelton for NameGenerator (facilitates uses as a webserver)
class SingletonNameGen:
    nameGenerator = None

    # Init singleton
    @staticmethod
    def initFromDatabase(ngram, database):
        SingletonNameGen.nameGenerator = NameGen(ngram)
        SingletonNameGen.nameGenerator.init(database)

    def initFromNgram(jsonFilenamePrefix):
        SingletonNameGen.nameGenerator = NameGen(ngram)
        SingletonNameGen.nameGenerator.loadFromFile(jsonFilenamePrefix)

    # Call generates method
    @staticmethod
    def gen():
        s = SingletonNameGen.nameGenerator.generate()[1:-1]
        return s
