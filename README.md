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
* `resources`: contains resource files, such as saved indeces.
* `service`: a python packages with services such as a search engine.
* `tests`: contains tests.
* `util`: a python package for a collection of utility functions such as reading and writing.
* `requirements.txt`: contains pip requirements.
* `command_line.sh`: answer to the command line question.

# Viewing Plots
Some plots are not displayed properly on GitHub. You can find a version of the notebook with everything displayed
[here](https://nbviewer.org/github/jonasbarth/adm-2022-hw-3/blob/main/main.ipynb).

# How to install the necessary `nltk` corpi.
```python
import nltk
nltk.download('stopwords', download_dir='./env/Lib/nltk_data')
nltk.download('punkt', download_dir='./env/Lib/nltk_data')
```
