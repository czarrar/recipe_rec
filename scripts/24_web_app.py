from flask import Flask, request, jsonify
from recipe_rec import RecipeRec
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
        nearest_recipe = recs.proximity_model(request.form['ingredients']) #dict
        name = list(nearest_recipe.keys())[0]
        val = list(nearest_recipe.values())[0]
        ret = ret.format(request.form['ingredients'])
        ret = ret + '<h2>Nearest Recipe</h2><p><b>{}:</b> {}</p>'.format(name, val)
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
