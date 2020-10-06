import requests
from flask import render_template, redirect, session, g, request, flash, abort
from flask_uploads import UploadNotAllowed

from config import app, images
from decorators import login_required
from forms import RecipeAddForm, LoginForm, RegisterForm
from recipes import Recipe
from utils import Paginate


@app.before_request
def before_request():
    if 'user_token' in session and 'username' in session:
        user_token = session['user_token']
        username = session['username']
        g.user_token = user_token
        g.username = username
    else:
        g.user_token = None
        g.username = None


@app.route('/recipes/')
def recipe_list_all():
    recipe = Recipe(api_url='https://recipes-cookbook-api.herokuapp.com/api/recipes/')
    response = recipe.get()
    recipes = response.json()
    paginate = Paginate(recipes, 'bootstrap4')
    pagination_recipes = paginate.get_data(offset=paginate.offset, per_page=paginate.per_page)
    pagination = paginate.pagination()
    return render_template('recipe_list_all.html', recipes=pagination_recipes, page=paginate.page,
                           per_page=paginate.per_page, pagination=pagination)


@app.route('/recipes/<string:username>/')
@login_required
def recipe_list_user(username):
    recipe = Recipe(api_url=f'https://recipes-cookbook-api.herokuapp.com/api/recipes/?author__username={username}')
    response = recipe.get()
    recipes = response.json()
    paginate = Paginate(recipes, 'bootstrap4')
    pagination_recipes = paginate.get_data()
    pagination = paginate.pagination()
    return render_template('recipe_list_user.html', recipes=pagination_recipes, page=paginate.page,
                           per_page=paginate.per_page, pagination=pagination)


@app.route('/recipes/<string:username>/<int:pk>/delete/', methods=['GET', 'POST', 'DELETE'])
@login_required
def recipe_delete(username, pk):
    recipe = Recipe(
        api_url=f'https://recipes-cookbook-api.herokuapp.com/api/recipes/{pk}/?author__username={username}',
        api_token=g.user_token
    )
    response = recipe.get()
    if response.status_code == 404 or username != g.username:
        abort(404)
    if request.method == 'POST':
        recipe.delete()
        flash('Successfully deleted recipe.')
        return redirect(f'/recipes/{username}/')
    return render_template('recipe_delete.html')


@app.route('/recipes/<string:username>/<int:pk>/edit/', methods=['GET', 'POST', 'PATCH'])
@login_required
def recipe_edit(username, pk):
    """!!!"""
    recipe = Recipe(
        api_url=f'https://recipes-cookbook-api.herokuapp.com/api/recipes/{pk}/?author__username={username}',
        api_token=g.user_token
    )
    response = recipe.get()
    if response.status_code == 200 and username == g.username:
        recipe_to_edit = response.json()
    else:
        recipe_to_edit = None
        abort(404)
    form = RecipeAddForm(data=recipe_to_edit)
    if form.validate_on_submit():
        try:
            if form.image.data != 'app/media/default.png':
                # if the user has uploaded a picture file
                image = images.save(form.image.data)
                image_path = f'app/media/recipe_images/{image}'
            else:
                # form.image.data by default is 'app/media/default.png'
                image_path = 'app/media/default.png'
        except UploadNotAllowed:
            # if the user uploaded a file that is not a picture
            flash('Incorrect picture format', 'error')
        else:
            recipe_data, recipe_files = recipe.get_form_data(form, image_path)
            recipe_id = recipe_to_edit['id']
            recipe.edit(recipe_data, recipe_files, recipe_id)
            return redirect('/recipes/')
    return render_template('recipe_edit.html', form=form)


@app.route('/recipes/add/', methods=['GET', 'POST'])
@login_required
def recipe_add():
    """!!!"""
    form = RecipeAddForm()
    if form.validate_on_submit():
        try:
            if form.image.data != 'app/media/default.png':
                # if the user has uploaded a picture file
                image = images.save(form.image.data)
                image_path = f'app/media/recipe_images/{image}'
            else:
                # form.image.data by default is 'app/media/default.png'
                image_path = 'app/media/default.png'
        except UploadNotAllowed:
            # if the user uploaded a file that is not a picture
            flash('Incorrect picture format', 'error')
        else:
            recipe = Recipe(
                api_url='https://recipes-cookbook-api.herokuapp.com/api/recipes/',
                api_token=g.user_token
            )
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
        response = requests.post(url='https://recipes-cookbook-api.herokuapp.com/api/auth/', json=payload)
        # response_data is token but in json format
        response_data = response.json()
        user_token = response_data.get('token', None)
        session['user_token'] = user_token
        if session['user_token'] is None:
            flash('Invalid username or password.', 'error')
        else:
            session['username'] = form.username.data
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/recipes/')
    return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        g.user_token = None
        g.username = None
        session['user_token'] = None
        session['username'] = None
        return redirect('/recipes/')
    return render_template('logout.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        payload = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'password2': form.password2.data
        }
        requests.post(url='https://recipes-cookbook-api.herokuapp.com/api/users/', json=payload)
        flash('The account has been successfully created.')
        return redirect('/login/')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
