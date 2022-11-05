import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def preprocess(desc: str):
    """Preprocesses a string so that it can be used in the inverted index.

    This function:
    - Removes stop words
    - Removes punctations
    - Tokenizes the string
    - Stems each word

    :returns
    a list of lower case, stemmed, words of the original string."""
    tokened_desc = word_tokenize(desc)

    lower_desc = list(map(lambda word: word.lower(), tokened_desc))
    no_stop_words_desc = list(filter(lambda word: word not in stop_words, lower_desc))
    cleaned_desc = list(filter(lambda word: word not in string.punctuation, no_stop_words_desc))

    stemmed = set(stemmer.stem(word) for word in cleaned_desc)
    return stemmed

