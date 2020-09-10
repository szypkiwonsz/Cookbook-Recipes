from flask import Flask, render_template

from recipes import Recipes

app = Flask(__name__)
r = Recipes


@app.route('/recipes/')
def recipe_list():
    recipes = r.get_recipes('https://recipes-cookbook-api.herokuapp.com/api/recipes/')
    return render_template('recipes.html', recipes=recipes)


if __name__ == '__main__':
    app.run()
