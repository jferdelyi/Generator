from .NameGenerator import NameGenerator

# Singelton for NameGenerator (facilitates uses as a webserver)


class SingletonNameGenerator:
    generator = None

    # Init singleton
    @staticmethod
    def init(database, selectedNgram):
        SingletonNameGenerator.generator = NameGenerator(database, selectedNgram)
        SingletonNameGenerator.generator.init()

    @staticmethod
    def reload(selectedNgram):
        SingletonNameGenerator.generator.reload(selectedNgram)

    # Call generates method
    @staticmethod
    def generate():
        return SingletonNameGenerator.generator.generate()[1:-1]
    
    @staticmethod
    def getSelectedNgram():
        return SingletonNameGenerator.generator.getSelectedNgram()
