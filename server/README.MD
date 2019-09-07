Server script (server.py) options:
* -ngram <number> set ngram for serving 
* -load <filname> load learning data from json
Default value use the database 'ville'
  
Generator script (generator.py) is used to create a new database from a list of words, options:
* -ngram <number> set ngram for learning
* -load <filname> load learning data from json

If you want to put a new database, create a new folder in data with the name of your database. Put your file inside named 'data.dat'
After thath you can execute the script <br />
`python generator.py -load <your_database_name> -ngram <ngram>`<br />
For exemple <br />
`python generator.py -load ville -ngram 10`<br />
