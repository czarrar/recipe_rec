# %% Packages
import os
os.chdir('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/scripts')

import recipe_rec
#import importlib
recipe_rec = importlib.reload(recipe_rec)

# %% Read in ingredients
recipe_file = '../data/20_ingredients.csv'
recs = recipe_rec.RecipeRec()
recs.load_from_csv(recipe_file)

# %% Apply TFIDF
recs.fit_model()

# %% Save
#!rm z_model.p
recs.save_model("z_model.p")

# %% Test loading it back
import numpy as np
recs2 = recipe_rec.RecipeRec.load_model('z_model.p')
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
tmp = recs.proximity_model(test_recipes[0], to_clean=False)
tmp
tmp.values()
