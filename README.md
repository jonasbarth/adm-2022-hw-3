# ADM 2022 HW 3
This repository contains the code for [Homework 3](https://github.com/lucamaiano/ADM/tree/master/2022/Homework_3) 
for [Algorithmic Methods for Data Mining 2022](http://aris.me/index.php/data-mining-ds-2022) at La Sapienza.

Contributors:
* Laura Mignella
* Paolo Barba
* Jonas Barth

# Structure
The repository contains:

* `main.ipynb`: a jupyter notebook that allows you to run the search engine.
* `domain`: a python package containing domain objects for this homework.
* `index`: a python package containing index classes used for searching.
* `parse`: a python package with logic for parsing `.html` pages from Atlas Obscura.
* `reader`: a python package for reading various files.
* `writer`: a python package for writing to files.
* `tests`: contains tests.
* `requirements.txt`: contains pip requirements.

# How to install the necessary `nltk` corpi.
```python
import nltk
nltk.download('stopwords', download_dir='./env/Lib/nltk_data')
nltk.download('punkt', download_dir='./env/Lib/nltk_data')
```
