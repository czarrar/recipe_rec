#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:17:53 2020

@author: Zarrar Shehzad
"""

import numpy as np
import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

import pickle

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
                      if not item in self._stop_words ]
        # TODO: use nlp('en_...') and then item.pos_ != "VERB" ]
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

# %% Recipe Rec
class RecipeRec(object):
    """Recipe Recommendations"""
    def __init__(self):
        self.model = Tfidf_Wrapper()
        self.ingredients = None
        return

    def load_from_csv(self, recipe_file):
        # recipe_file = ../data/20_ingredients.csv
        recipes = pd.read_csv(recipe_file)
        # Change '^' to a comma and get out a list of recipe ingredients
        ingredients = [ x.replace('^', ', ') for x in recipes.ingredients ]
        self.ingredients = np.array(ingredients)
        return

    def save_model(self, ofile):
        pickle.dump( favorite_color, open( "save.p", "wb" ) )

    def fit_model(self):
        if self.ingredients is None:
            raise Exception('Please load and build the model first')
        self.model_features = self.model.fit_transform(self.ingredients)
        return self.model_features

    def vectorize_ingredients(self, str_ingredients):
        # First project those ingredients into the term frequency space
        vec_ingredients = self.model.transform(str_ingredients)
        return vec_ingredients

    # What is it that I want to input here?
    # Input: A vectorized recipe
    # Process: Use nearest neighbor approach to find recipes most similar to input
    # Output: List of most similar recipes in ranked order
    def proximity_model(self, str_ingredients, top_n=1):
        # Todo: check that str_ingredients is a string

        # Vectorize the input ingredients
        vec_ingredients = self.vectorize_ingredients([str_ingredients])

        # Get the similarities between the input ingredients and the model
        cosims = cosine_similarity(self.model_features, vec_ingredients)

        # Get the order of ingredients in model most similar to the inputs
        inds = np.argsort(cosims, axis=None)[::-1]

        # Get the x top ingredients
        nearest_ingredients = self.ingredients[inds[:top_n]]

        return(nearest_ingredients)
