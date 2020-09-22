# %% Do it
# This script will generate the recipes to show the user

#import os
#os.chdir('/Users/czarrar/Dropbox/Circle/Jerb/recipe_rec/code')

import numpy as np
from libs_recipe_recs import RecipeRec

class PairedChoices(object):
    """
    Deals with displaying the paired choices to the user.
    """

    def __init__(self):
        self.recs = RecipeRec.load_model('z_model.p')

        self.recipes = self.recs.recipes
        self.recipes['group'] = np.loadtxt('z_kmeans25.txt')
        self.recipes['group'] = self.recipes.group.astype('category')
        self.n_recipes = self.recipes.shape[0]

        return

    def log_choices(self, prior_choices):
        """
        This will incorporate the last set of choices

        Parameters
        ----------
        prior_choices : dict
            A json output from the front-end
        """


        return

    def gen_choices(self, k=10):
        """
        Generates the new set of choices to show the user. Returns a json or
        dictionary with list of pairs, etc.
        """

        # Ensure that k items to show is even
        # This always every item to be paired with another item
        if (k % 2) > 0:
            print('Setting k = k + 1')
            k = k + 1

        # Which of the groups to show
        grps = np.random.choice(self.recipes.group.cat.categories, k)

        # Get the indices from recipes to get from
        inds = [
            np.random.choice(self.recipes.index[self.recipes.group==g], 1)[0]
            for g in grps
        ]
        inds = np.random.permutation(inds)

        # Put together the pairs of items in each choice
        pairs = inds.reshape((k//2, 2))

        # Return back all the information useful for the front-end
        select_cols = ['recipe_id', 'name', 'ingredients', 'img_path']
        formatted_pairs = []
        for i in range(pairs.shape[0]):
            left  = self.recipes.loc[pairs[i,0],select_cols].to_dict()
            right = self.recipes.loc[pairs[i,1],select_cols].to_dict()
            formatted_pairs.append({'left': left, 'right': right})

        return(formatted_pairs)



class RecommendRecipes(object):
    '''
    Recommend 3 recipes for a user.
    '''

    def __init__(self):
        self.recs = RecipeRec.load_model('z_model.p')

        self.recipes = self.recs.recipes
        self.recipes['group'] = np.loadtxt('z_kmeans25.txt')
        self.recipes['group'] = self.recipes.group.astype('category')
        self.n_recipes = self.recipes.shape[0]


    def topk(self, k=3):
        '''Returns a dict or json of the k recipes to recommend.'''
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
