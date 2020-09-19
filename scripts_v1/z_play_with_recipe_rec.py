import spacy
import pandas as pd

nlp = spacy.load('en_core_web_sm')

recipe_file = '../data/20_ingredients.csv'
recipes = pd.read_csv(recipe_file)
ingredients = recipes.ingredients[0].replace('^', ', ')

doc = nlp(ingredients)
doc

# Tokenize, clean, and return lemmatized word
tokens = [ token.lemma_ for token in doc
    if token.is_stop != True    # no stop words
    and token.pos_ != 'VERB'    # no verbs
    and token.is_punct != True  # no punctuation
    and token.is_digit != True  # no digits
    and len(token) > 1          # no characters
]
tokens

token.is_dig
