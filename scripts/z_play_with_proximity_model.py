# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# %% Packages
import os
os.chdir('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/scripts')

from recipe_rec import RecipeRec
import recipe_rec
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import importlib
recipe_rec = importlib.reload(recipe_rec)

import nltk

# %% Read in ingredients
recipe_file = '../data/20_ingredients.csv'
recs = recipe_rec.RecipeRec()
recs.load_from_csv(recipe_file)

# %% Apply TFIDF
recs.fit_model()

# %% Save
recs.save_model('z_model.p')

recs2 = recipe_rec.RecipeRec()
recs2.load_from_pickle('z_model.p')
np.all(recs.model.features == recs2.model.features)

# %% Test Recipes + Try Out a Simple Proximity Model
test_recipes = [
  'caramels water chopped pecans Rice Krispies milk chocolate chips shortening',
 'peanut butter sugar large egg room temperature vanilla extract milk chocolate kisses',
 'semisweet chocolate chips, water, large egg yolk lightly beaten, teaspoons vanilla extract, heavy whipping cream, sugar, Whipped cream, raspberries',
 'dried minced onion, salt, chili powder, cornstarch, ground cumin, red pepper flakes, cayenne pepper, dried minced garlic, dried oregano, ground beef, water',
 'reduced-sodium soy sauce, rice wine vinegar, cornstarch, sesame oil, divided, pork tenderloin, cut into strips, red chile pepper, chopped, cloves garlic, minced, onion, chopped, green bell pepper, chopped, head bok choy, leaves and stalks separated, chopped, crowns broccoli, chopped, ground ginger',
 'Ingredient Checklist, hoisin sauce, brown sugar, soy sauce, applesauce, pork loin, sliced, cut into thin strips, cornstarch, peanut oil, sesame oil, chopped fresh ginger root, broccoli florets'
]


# %% Compute Cosine Similarity
recs.proximity_model(test_recipes[1], to_clean=False)

# Now you want to compute all the similarities
## Try the cosine first
from sklearn.metrics.pairwise import cosine_similarity
sims = cosine_similarity(features, row.to_numpy()[np.newaxis, ...])

## We can order the output to get the largest items first
inds = np.argsort(sims, axis=None)[::-1]

## And now that we have this, we can extract out the ingredients
## This mostly looks good as it's a bunch of dessert items
ingredients[inds[:3]]


# %% Compute Euclidean Distance

# And then pick the top one
from sklearn.metrics.pairwise import euclidean_distances
ds = euclidean_distances(features, row.to_numpy()[np.newaxis, ...])

## Here want smallest item first
inds2 = np.argsort(ds, axis=None) # inds2 is mostly similar to inds above

ingredients[inds2[:3]]


# %% Try out specific foods
# I'm interested in if I try to find the similarity between food items
# Okay this didn't add anything new at all

## DIDNT FINISH DOING THIS

terms = ['chicken', 'steak', 'apple', 'orange', 'lettuce', 'pepper', 'tomato', 'brownie', 'cookie']
term_inds = [ tfidf.vectorizer.vocabulary_[item] for item in terms ]
term_inds

term_mat = features.iloc[:,term_inds]
term_mat

## sims for all terms (same idea)
csims = cosine_similarity(term_mat.T)
csims.round(3)
.shape

## get out the smallest item first
for i in sims.shape[1]:
    inds = np.argsort(sims[:,i], axis=None)[::-1]
    print(features.columns[inds[:10]])
