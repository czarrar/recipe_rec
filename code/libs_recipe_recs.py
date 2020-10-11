#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:17:53 2020

@author: Zarrar Shehzad
"""

import numpy as np
import spacy
import nltk, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

import pickle

class Tfidf_Wrapper(object):
    """
    """

    def __init__(self):
        #self.nlp = spacy.load('en_core_web_sm')
        self.docs = None
        self.features = None
        self.features_test = None

        # For removing stop words like 'the'
        self._stop_words = set(nltk.corpus.stopwords.words('english'))
        # For lemmatizing (e.g., thinking => think)
        self._lemmatizer = WordNetLemmatizer()

        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize, use_idf=True)
        return

    # I need to remove stop words before I lem otherwise there will be a mismatch
    def _tokenize(self, text):
        """
        Takes text and tokenizes. Removes stop words, verbs, punctuations,
        digits, and characters. Lemmatizes the token as well.

        Parameters
        ----------
        text : str
            String to tokenize

        Returns
        -------
        tokens : list
        """
        #doc = self.nlp(text)

        # Tokenize, clean, and return lemmatized word
        #tokens = [ token.lemma_ for token in doc
        #    if token.is_stop != True    # no stop words
        #    and token.pos_ != 'VERB'    # no verbs
        #    and token.is_punct != True  # no punctuation
        #    and token.is_digit != True  # no digits
        #    and len(token.text) > 1     # no characters
        #]

        # Remove digits and punctuation
        text = re.sub('[\W0-9]+',' ', text)

        # Tokenize
        tokens = nltk.word_tokenize(text)

        # Remove verbs
        #tokens = [ item for item,tag in nltk.pos_tag(tokens) if tag[0] != 'V' ]

        # Remove stop words and characters
        tokens = [ item for item in tokens
                    if len(item) > 1
                    if not item in self._stop_words ]

        # Lemmatize
        lems = [ self._lemmatizer.lemmatize(item) for item in tokens ]

        return lems

    def fit_transform(self, docs, reduce=True):
        self.docs = docs
        X = self.vectorizer.fit_transform(docs).toarray()

        if reduce == True:
            pca = PCA(n_components = 0.95)
            X_reduced = pca.fit_transform(X)
            self.features = pd.DataFrame(X_reduced, dtype='float32')
        else:
            self.features = pd.DataFrame(X,
                columns = self.vectorizer.get_feature_names(),
                dtype='float32')

        return self.features

    def transform(self, docs):
        Xtest = self.vectorizer.transform(docs)
        self.features_test = pd.DataFrame(Xtest.toarray(), columns = self.vectorizer.get_feature_names())
        return self.features_test


# %% Recipe Rec
class RecipeRec(object):
    """Recipe Recommendations"""
    def __init__(self):
        self.model = Tfidf_Wrapper()
        self.recipes = None
        self.nlp = spacy.load('en_core_web_sm')
        return

    def _clean_ingredients(self, text):
        doc = self.nlp(text)
        items = [ token.text for token in doc
            if token.is_stop != True    # no stop words
            and token.pos_ != 'VERB'    # no verbs
            and token.is_punct != True  # no punctuation
            and token.is_digit != True  # no digits
        ]
        ingredients = ' '.join(items)
        return ingredients

    def read_csv(self, recipe_file, to_clean=False, *args, **kwargs):
        # recipe_file = ../data/20_ingredients.csv
        self.recipes = pd.read_csv(recipe_file, *args, **kwargs)
        if to_clean:
            ingredients = [ self._clean_ingredients(ingredients) for ingredients in self.recipes.ingredients ]
            self.recipes['ingredients'] = ingredients
        return

    def save_model(self, ofile):
        pickle.dump({'features': self.model.features, 'docs': self.model.docs,
                        'recipes': self.recipes}, open( ofile, "wb" ) )

    @classmethod
    def load_from_file(cls, ifile):
        dat = pickle.load( open(ifile, "rb") )
        recs = cls()
        recs.model.docs = dat['docs']
        recs.model.features = dat['features']
        recs.recipes = dat['recipes']
        return recs

    def fit_model(self, reduce=True):
        if self.recipes is None:
            raise Exception('Please load and build the model first')
        self.model.fit_transform(self.recipes.ingredients, reduce)
        return

    def vectorize_ingredients(self, str_ingredients):
        # First project those ingredients into the term frequency space
        vec_ingredients = self.model.transform(str_ingredients)
        return vec_ingredients

    # What is it that I want to input here?
    # Input: A vectorized recipe
    # Process: Use nearest neighbor approach to find recipes most similar to input
    # Output: List of most similar recipes in ranked order
    def proximity_model(self, str_ingredients, top_n=1, to_clean=False):
        """
        Takes ingredients for a recipe and returns the closest recipes in the
        current recipe book.

        Parameters
        ----------
        str_ingredients : str
            Search for the nearest recipe with the following ingredients

        top_n : int
            How many results to return (default: 1)

        to_clean : bool
            If you want to clean the output ingredients (default: False)
            This includes: removing characters, stop words, puntuations, digits,
            and verbs.

        Returns
        -------
        recipe_ids : pd.Series
        """
        # Todo: check that str_ingredients is a string
        if type(str_ingredients) != str:
            raise Exception("Input type must be string")

        # Vectorize the input ingredients
        vec_ingredients = self.vectorize_ingredients([str_ingredients])

        # Get the similarities between the input ingredients and the model
        cosims = cosine_similarity(self.model.features, vec_ingredients)

        # Get the order of ingredients in model most similar to the inputs
        inds = np.argsort(cosims, axis=None)[::-1]

        # Get the x top ingredients
        nearest_ingredients = []

        # Get the recipes
        nearest_recipes = self.recipes.iloc[inds[:top_n],:]

        # Clean the ingredients
        if to_clean:
            nearest_recipes['ingredients'] = [
                self._clean_ingredients(txt)
                    for txt in nearest_recipes.ingredients
            ]

        return nearest_recipes
