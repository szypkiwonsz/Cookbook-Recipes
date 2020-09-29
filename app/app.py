import requests
from flask import render_template, redirect, session, g, request, flash

from config import app, images
from decorators import login_required
from forms import RecipeAddForm, LoginForm
from recipes import Recipe
from utils import Paginate


@app.before_request
def before_request():
    if 'user_token' in session:
        user_token = session['user_token']
        g.user_token = user_token
    else:
        g.user_token = None


@app.route('/recipes/')
def recipe_list():
    recipe = Recipe(url_get_post='https://recipes-cookbook-api.herokuapp.com/api/recipes/')
    response = recipe.get()
    recipes = response.json()
    paginate = Paginate(recipes, 'bootstrap4')
    pagination_recipes = paginate.get_data()
    pagination = paginate.pagination()
    return render_template('recipe_list.html', recipes=pagination_recipes, page=paginate.page,
                           per_page=paginate.per_page, pagination=pagination)


@app.route('/recipes/add/', methods=['GET', 'POST'])
@login_required
def recipe_add():
    form = RecipeAddForm()
    if form.validate_on_submit():
        if form.image.data != 'app/media/default.png':
            image = images.save(form.image.data)
            image_path = f'app/media/recipe_images/{image}'
        else:
            image_path = form.image.data
        recipe = Recipe(url_get_post='https://recipes-cookbook-api.herokuapp.com/api/recipes/', api_token=g.user_token)
        recipe_data, recipe_files = recipe.get_form_data(form, image_path)
        recipe.add_new(recipe_data, recipe_files)
        return redirect('/recipes/')
    return render_template('recipe_add.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }
        response = requests.post('https://recipes-cookbook-api.herokuapp.com/api/auth/', json=payload)
        user_token = response.json().get('token', None)
        session['user_token'] = user_token
        if session['user_token'] is None:
            flash('Invalid username or password.', 'error')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/recipes/')
    return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        g.user_token = None
        session['user_token'] = None
        return redirect('/recipes/')
    return render_template('logout.html')


if __name__ == '__main__':
    app.run()
