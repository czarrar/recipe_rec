#import os
#os.chdir('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/code')

import pandas as pd
import numpy as np
from libs_recipe_recs import RecipeRec

class RecommendRecipes(object):
    '''
    Recommend 3 recipes for a user.
    '''

    def __init__(self, user_ratings=None):
        self.recs = RecipeRec.load_model('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/code/z_model.p')

        self.recipes = self.recs.recipes
        self.recipes['group'] = np.loadtxt('z_kmeans25.txt')
        self.recipes['group'] = self.recipes.group.astype('category')
        self.n_recipes = self.recipes.shape[0]

        self.user_ratings = user_ratings

    def topk_user(self, uid, k=3, minRating=4):
        '''
        1a. Restricts the user ratings to only the training data
        1b. Restricts the user ratings to those that are 4 or higher
        2. Get the suggestions from the proximity model
        '''
        uratings = self.user_ratings[self.user_ratings.user_id == uid]
        # Restrict to training data and ratings > 4
        inds = ((uratings.training==1) & (uratings.rating>=minRating))
        selected_ratings = uratings[inds]
        # Get the ingredients for this users ratings
        selected_ratings = pd.merge(selected_ratings,
            self.recipes[['recipe_id', 'ingredients']], how='left', on='recipe_id')
        prior_ingredients = ", ".join(selected_ratings.ingredients)
        # Get the recommended recipes
        user_recs = self.recs.proximity_model(prior_ingredients, top_n=k)

        return user_recs

    def topk_group(self, k=3, minRating=4.5, minNRatings=100):
        '''
        This will return a generic recommendation based on average ratings.
        Returns a dict or json of the k recipes to recommend.
        '''
        # Imagine our only prior are the average prior ratings

        # Let's select some top subset of the recipes
        inds = (self.recipes.ave_rating > 4.5) & (self.recipes.num_reviews > 100)
        recipes_select = self.recipes[inds]

        # Of that subset, we randomly select the recipes to show the user
        # Return a list of dictionaries
        rids = np.random.choice(recipes_select.index, k, replace=False)
        scols = ['recipe_id', 'name', 'ingredients', 'img_path']
        recipes_to_show = recipes_select.loc[rids,scols].to_dict('records')

        return recipes_to_show


#class RecommenderMetrics:
