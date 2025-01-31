from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV data
csv_file = "recipes.csv"  # Change this to your actual file name
df = pd.read_csv(csv_file)

def get_recipe_details(recipe_name):
    # Search for the recipe
    recipe = df[df['Recipes'].str.lower() == recipe_name.lower()]
    
    if recipe.empty:
        return None
    
    ingredients = recipe['ingredients'].values[0]
    directions = recipe['directions'].values[0]
    
    return {"Ingredients": ingredients, "Directions": directions}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    recipe_name = request.args.get('recipe_name')
    if not recipe_name:
        return jsonify({"error": "Please provide a recipe name."}), 400
    
    recipe_details = get_recipe_details(recipe_name)
    
    if not recipe_details:
        return jsonify({"error": "Recipe not found. Please try another name."}), 404
    
    return jsonify(recipe_details)

if __name__ == '__main__':
    app.run(debug=True)