from flask import Flask, request, jsonify
from recipe_rec import RecipeRec
import numpy as np
import traceback

app = Flask(__name__)

@app.route('/proximity', methods=['GET', 'POST'])
def proximity():
    if request.method == 'POST':
        try:
            dat = request.json
            nearest_recipe = recs.proximity_model(dat['ingredients']) #dict
            return jsonify(nearest_recipe)
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Please give me some inputs')

@app.route('/proximity_form', methods=['GET', 'POST'])
def proximity_form():
    ret = '''<form method="POST">
                  Ingredients: <input type="text" name="ingredients" size=100 value="{}"><br />
                  <input type="submit" value="Submit"><br>
              </form>'''
    if request.method == 'POST':
        # Save the input ingredients
        ret = ret.format(request.form['ingredients'])

        # Get the nearest recipe
        nearest_recipe = recs.proximity_model(request.form['ingredients'])
        d = nearest_recipe.iloc[0,:].to_dict()
        d['ave_rating'] = np.round(d['ave_rating'], 1)

        # Template html output
        out = '<h2>Nearest Recipe</h2>\
                <img src="{img_path}" />\
                <p><b>Name:</b> {name}</p>\
                <p><b>Ingredients:</b> {ingredients}</p>\
                <p><b>Ave Rating:</b> {ave_rating} stars (out of {num_reviews} reviews)</p>'

        # Add to html output
        ret = ret + out.format(**d)
        #request2 = requests.post(request.form)
        #ret.format(ingredients = request2.json['ingredients'])
    else:
        ret = ret.format(' ')
    return ret


if __name__ == "__main__":
    # Load in the model
    recs = RecipeRec.load_model('z_model.p')
    # Run the app
    app.run(debug=True)
