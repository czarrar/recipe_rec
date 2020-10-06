# %% Packages
import os
os.chdir('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/code')

import libs_choices_backend
import importlib
libs_choices_backend = importlib.reload(libs_choices_backend)

pc = libs_choices_backend.PairedChoices()

pc.gen_choices(k=2)

prior_choices = {
    'pairs': [
        {
            'left': 123, # recipe id
            'right': 345, # recipe id
            'winner': 'left',
            'time': 238749823 # some integer time-stamp
            'response_time': 900 # in milliseconds
        }
    ],
    'session_id': 'XYZ'
}




# %% Play with next
rr = libs_choices_backend.RecommendRecipes()
rr.topk()
