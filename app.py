from flask import Flask, render_template
from recipes import Recipes

app = Flask(__name__)
r = Recipes


@app.route('/')
def index():
    recipes = r.get_recipes('https://recipes-cookbook-api.herokuapp.com/api/recipes/')
    print(recipes)
    return render_template('index.html', recipes=recipes)


if __name__ == '__main__':
    app.run()
