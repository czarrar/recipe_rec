# %% Packages
import os
os.chdir('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/code')

import libs_recipe_recs
#import importlib
#recipe_rec = importlib.reload(libs_recipe_recs)

# %% Read in ingredients
recipe_file = '../data/30_ingredients+ave_ratings.csv'
recs = libs_recipe_recs.RecipeRec()
recs.load_from_csv(recipe_file, index_col=0)

# %% Apply TFIDF
recs.fit_model()

# %% Save
#!rm z_model.p
recs.save_model("z_model.p")

# %% Test loading it back
import numpy as np
recs2 = libs_recipe_recs.RecipeRec.load_model('z_model.p')
np.all(recs.model.features == recs2.model.features)

recs2.recipes.query('recipe_id == 233786').ingredients.tolist()[0]
