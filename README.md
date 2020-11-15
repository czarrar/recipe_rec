# Recipe Recommendation App

This is an app-in-progress that collects user preferences for different recipes in real-time and then recommends new recipes for the user to try. For details on the project proposal please refer to this page: https://write.as/a-to-z/revised-project-proposal.

## Overview

**Problem:** You are a startup that provides people with recipes and the ingredients to make delicious home-cooked meals (e.g., blue apron). With the pandemic more people are staying home and cooking, increading demand and competition. To keep up with the competition, you want to provide customers with personalized meal recommendations that ensure they would stick with your business.

**Goal:** Have a recommendation engine that is 50% more likely to recommend a recipe + ingredients that a customer will want to receive in the mail relative to a standard approach.

**Approach:** This will be a web app where people will first indicate whether they like particular meals (image with ingredients). To facilitate this choice, we will show pairs of recipes and users will select the recipe they like better. The recipe ingredients will be represented using some form of word embedding, allowing comparison between recipes. The user interface will be made in Flask with JavaScript. The backend (rec engine) will use Python.

## Recipe Data

Recipe data is taken from https://www.kaggle.com/elisaxxygao/foodrecsysv1. The data reflects 52,821 recipes from 27 categories posted on allrecipes.com between 2000 and 2018. For each recipe, they collected the ingredients, image and the corresponding ratings from users.

### Process Data

We want to represent each recipe as a vector. The file `code/20_Recipes_to_TFIDF.py` takes the input recipes, cleans the data, and used TFIDF to represent the ingredients. Data cleaning includes removal of digits, punctuation, stop words, and characters, and lemmatization of each word. The sklearn class `TfidfVectorizer` is then used to generate the inverse term frequency for each ingredient in a recipe.

Given that there are thousands of recipes, we can perform dimensionality reduction to group the recipes together in a meaningful way. This is done in `scripts_v2/22_viz_tfidf.ipynb`. PCA is first applied to the TFIDF vectors in order to reduce the dimensionality of the features (from ~3k word vocabulary to ~1k components), and then k-means is applied to the PCA-reduced data and the silhouette width is used to determine the ideal cluster number.

## App

The Flask app is located in `code/b_web_app.py`. Presently it shows a pair of recipe images to the user and gets their response.
