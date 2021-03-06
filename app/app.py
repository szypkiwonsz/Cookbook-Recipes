import requests
from flask import render_template, redirect, session, g, request, flash, abort
from flask_uploads import UploadNotAllowed

from config import app, images, DEFAULT_RECIPE_IMAGE_PATH
from decorators import login_required
from forms import RecipeAddForm, LoginForm, RegisterForm
from recipes import RecipeManager
from utils import Paginate, delete_image_file


@app.before_request
def before_request():
    """A function that checks if the user is logged in."""
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
    """Page listing all recipes."""
    recipe_manager_handler = RecipeManager()
    recipes = recipe_manager_handler.get_all_recipes_response().json()
    # paginating list of recipes
    paginate = Paginate(recipes, 'bootstrap4')
    pagination_recipes = paginate.get_data(offset=paginate.offset, per_page=paginate.per_page)
    pagination = paginate.pagination()

    return render_template('recipe_list_all.html', recipes=pagination_recipes, page=paginate.page,
                           per_page=paginate.per_page, pagination=pagination)


@app.route('/')
def home_page():
    """Application home page."""
    return render_template('home_page.html')


@app.route('/recipes/<string:username>/')
def recipe_list_user(username):
    """Page listing user recipes."""
    recipe_manager = RecipeManager()
    recipes = recipe_manager.get_user_recipes_response(username).json()
    # if the user is not the author and there are no recipes displays the information
    if not recipes and g.username != username:
        flash('The user does not exist or has no recipes.')
    # paginating list of recipes
    paginate = Paginate(recipes, 'bootstrap4')
    pagination_recipes = paginate.get_data()
    pagination = paginate.pagination()

    return render_template('recipe_list_user.html', recipes=pagination_recipes, page=paginate.page,
                           per_page=paginate.per_page, pagination=pagination)


@app.route('/recipes/<string:username>/<int:pk>/delete/', methods=['GET', 'POST', 'DELETE'])
@login_required
def recipe_delete(username, pk):
    """Page confirming the removal of the recipe."""
    recipe_manager = RecipeManager(api_token=g.user_token)
    response = recipe_manager.get_user_recipe_response(username, pk)
    recipes = response.json()
    # shows 404 if there is no recipe to delete, api status code is 404 or username is not the author
    if not recipes or response.status_code == 404 or username != g.username:
        abort(404)
    # POST method handler
    if request.method == 'POST':
        recipe_manager.delete(pk, username)
        flash('Successfully deleted recipe.')
        return redirect(f'/recipes/{username}/')

    return render_template('recipe_delete.html')


@app.route('/recipes/<int:pk>/')
def recipe_detail(pk):
    """Page showing selected recipe."""
    recipe_manager = RecipeManager()
    response = recipe_manager.get_recipe_response(pk)
    recipe = response.json()
    # shows 404 if there is no recipe or response status code is 404
    if not recipe or response.status_code == 404:
        abort(404)

    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/recipes/<string:username>/<int:pk>/edit/', methods=['GET', 'POST', 'PATCH'])
@login_required
def recipe_edit(username, pk):
    """Page showing the possibility to edit the recipe."""
    recipe_manager = RecipeManager(api_token=g.user_token)
    response = recipe_manager.get_recipe_response(pk)
    recipe = response.json()
    # shows 404 if there is no recipe, response status code is 404 or user is not the author
    if not recipe or response.status_code == 404 or username != g.username:
        abort(404)
    # checking form validation
    form = RecipeAddForm(data=recipe)
    if form.validate_on_submit():
        try:
            if form.image.data != DEFAULT_RECIPE_IMAGE_PATH:  # if the user has uploaded a picture file
                image = images.save(form.image.data)
                image_path = f'app/media/recipe_images/{image}'
            else:
                image_path = None  # set image_path to None so as not to alter the image
        except UploadNotAllowed:  # if the user uploaded a file that is not a picture
            flash('Incorrect picture format', 'error')
        else:  # if there is no exception edit recipe data and image
            recipe_data, recipe_files = recipe_manager.get_form_data(form, image_path)
            recipe_manager.edit(recipe_data, recipe_files, pk, username)
            return redirect('/recipes/')

    return render_template('recipe_edit.html', form=form)


@app.route('/recipes/add/', methods=['GET', 'POST'])
@login_required
def recipe_add():
    """Page showing the possibility to add the recipe."""
    # checking form validation
    form = RecipeAddForm()
    if form.validate_on_submit():
        try:
            if form.image.data != DEFAULT_RECIPE_IMAGE_PATH:  # if the user has uploaded a picture file
                image = images.save(form.image.data)
                image_path = f'app/media/recipe_images/{image}'
            else:
                image_path = DEFAULT_RECIPE_IMAGE_PATH  # form.image.data by default is 'app/media/default.png'
        except UploadNotAllowed:  # if the user uploaded a file that is not a picture
            flash('Incorrect picture format', 'error')
        else:  # if there is no exception add new recipe
            recipe_manager = RecipeManager(api_token=g.user_token)
            recipe_data, recipe_files = recipe_manager.get_form_data(form, image_path)
            recipe_manager.add(recipe_data, recipe_files)  # adds new recipe
            image_file = recipe_files['image'][1]
            delete_image_file(image_file, image_path)  # deleting image file from local storage when it's uploaded
            return redirect('/recipes/')

    return render_template('recipe_add.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Application login page."""
    # checking form validation
    form = LoginForm()
    if form.validate_on_submit():
        # getting user token
        payload = {'username': form.username.data, 'password': form.password.data}
        json_response = requests.post(url='https://recipes-cookbook-api.herokuapp.com/api/auth/', json=payload).json()
        user_token = json_response.get('token', None)  # getting token from json response
        # load token to session variable
        session['user_token'] = user_token
        if session['user_token'] is None:  # if there is no token from response shows an error message
            flash('Invalid username or password.', 'error')
        else:  # if there is token from response load username to session variable
            session['username'] = form.username.data
            next_page = request.args.get('next')  # redirect to the page that was to be showed
            return redirect(next_page) if next_page else redirect('/recipes/')

    return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    """Application logout page."""
    # when POST -> setting g and session variables to none when logged out
    if request.method == 'POST':
        g.user_token = None
        g.username = None
        session['user_token'] = None
        session['username'] = None
        return redirect('/recipes/')

    return render_template('logout.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Application register page."""
    form = RegisterForm()
    # checking form validation
    if form.validate_on_submit():
        # registering user
        payload = {'username': form.username.data, 'email': form.email.data, 'password': form.password.data,
                   'password2': form.password2.data}
        response = requests.post(url='https://recipes-cookbook-api.herokuapp.com/api/users/', json=payload)
        if response.status_code != 201:
            for error_messages in response.json().values():
                flash(str(error_messages[0]))
        else:
            flash('The account has been successfully created.')
            return redirect('/login/')

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
