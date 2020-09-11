import os

from flask import Flask, render_template, redirect

from forms import RecipeAddForm
from recipes import Recipes

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

r = Recipes()


@app.route('/recipes/')
def recipe_list():
    recipes = r.get_recipes('https://recipes-cookbook-api.herokuapp.com/api/recipes/')
    return render_template('recipe_list.html', recipes=recipes)


@app.route('/recipes/add/', methods=['GET', 'POST'])
def recipe_add():
    form = RecipeAddForm()
    if form.validate_on_submit():
        return redirect('/recipes')
    return render_template('recipe_add.html', form=form)


if __name__ == '__main__':
    app.run()
