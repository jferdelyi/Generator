<h3>General</h3>

Generator script (generator.py) is an offline script, input:
* -ngram <number> set ngram for learning
* -load <filname> load learning data from json

When the script is running, press 'enter' to generate new result or 'q' to quit

<h3>Dependencies</h3>

* Python 3

<h3>Exemple</h3>

The database 'ville' in data folder as following: 
```bash
data
\---ville
     \---data.dat
```
Execute: `python generator.py -load ville -ngram 10`, the result:
```bash
data
\---ville
     |---data.dat
     \---generated
         |---ville.json
         |---ville_freq_2.json
         ...
         \---ville_freq_10.json
```

<h3>Custom database</h3>

If you want to put a new database:
* create a new folder in data folder named <your_database_name>
* put your file inside named 'data.dat'
* execute the script `python generator.py -load <your_database_name> -ngram <ngram>`
* change 'config.json' by your database informations

The file data.dat need to be a list of words as following:
```bash
TOULOUSE
PARIS
ARNAC LA POSTE
BOURG LA REINE
FOURQUEUX
CERE LA RONDE
```
