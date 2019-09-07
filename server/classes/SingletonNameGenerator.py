from .NameGenerator import NameGenerator

# Singelton for NameGenerator (facilitates uses as a webserver)


class SingletonNameGenerator:
    generator = None

    # Init singleton
    @staticmethod
    def init(database, ngram):
        SingletonNameGenerator.generator = NameGenerator(ngram)
        SingletonNameGenerator.generator.createDatabase(database)

    @staticmethod
    def initFromFile(database, ngram=-1):
        SingletonNameGenerator.generator = NameGenerator(ngram)
        return SingletonNameGenerator.generator.loadFromFile(database)

    @staticmethod
    def reload(database, ngram):
        SingletonNameGenerator.generator.reload(database, ngram)

    # Call generates method
    @staticmethod
    def gen():
        s = SingletonNameGenerator.generator.generate()[1:-1]
        return s
