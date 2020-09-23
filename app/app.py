import os

from flask import Flask, render_template, redirect
from flask_uploads import configure_uploads, IMAGES, UploadSet

from forms import RecipeAddForm
from recipes import Recipe

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOADED_IMAGES_DEST'] = 'media/recipe_images'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

recipe = Recipe(url_get_post='https://recipes-cookbook-api.herokuapp.com/api/recipes/',
                api_token='7863a78eadb90301bb98c7d4d06cbe497d92b756')


@app.route('/recipes/')
def recipe_list():
    recipes = recipe.get()
    return render_template('recipe_list.html', recipes=recipes)


@app.route('/recipes/add/', methods=['GET', 'POST'])
def recipe_add():
    form = RecipeAddForm()
    if form.validate_on_submit():
        if form.image.data != 'media/default.png':
            image = images.save(form.image.data)
            image_path = f'media/recipe_images/{image}'
        else:
            image_path = form.image.data
        recipe_data, recipe_files = recipe.get_form_data(form, image_path)
        recipe.add_new(recipe_data, recipe_files)
        return redirect('/recipes/')
    return render_template('recipe_add.html', form=form)


if __name__ == '__main__':
    app.run()
