French city name generator

How to use it:
    run 'python server.py'
    options:
		* -ngram <number> Set ngram for learning (default value is 4 ngram)
        * -save <filname> Saves the learning in JSON files
        * -load <filname> Load learning data from json
        * -gen <count> Generates count names and output in stdin, only if -noweb is specified

    Just serving
    run 'FLASK_APP=server.py flask run'
