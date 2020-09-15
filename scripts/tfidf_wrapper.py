import nltk
#import string
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer

class Tfidf_Wrapper(object):
    def __init__(self):
        # For removing stop words like 'the'
        self._stop_words = set(nltk.corpus.stopwords.words('english'))
        # For lemmatizing (e.g., thinking => think)
        self._lemmatizer = WordNetLemmatizer()
        # Create the TfidfVectorizer
        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize, use_idf=True)
        return

    # I need to remove stop words before I lem otherwise there will be a mismatch
    def _tokenize(self, text):
        #text   = text.translate(self._table) # remove punctuation + digits
        # Remove punctuations, digits, symbols
        text = re.sub('[\W0-9]+',' ', text)
        # Tokenize
        tokens = nltk.word_tokenize(text)
        # Remove single characters, stop words, and verbs
        tokens = [ item for item in tokens 
                      if len(item) > 1 
                      if not item in self._stop_words :
                      if item.pos_ != "VERB"
                 ]
        # Lemmatize
        lems = [ self._lemmatizer.lemmatize(item) for item in tokens ]
        return lems
    
    def fit_transform(self, docs):
        self._X = self.vectorizer.fit_transform(docs)
        self.features = pd.DataFrame(self._X.toarray(), columns = self.vectorizer.get_feature_names())
        return self.features

    def transform(self, docs):
        self._Xtest = self.vectorizer.transform(docs)
        self.features_test = pd.DataFrame(self._Xtest.toarray(), columns = self.vectorizer.get_feature_names())
        return self.features_test
