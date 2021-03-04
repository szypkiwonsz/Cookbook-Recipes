import os

from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads

# Configuration of app

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

# Configuration of images

app.config['UPLOADED_IMAGES_DEST'] = 'app/media/recipe_images'
DEFAULT_RECIPE_IMAGE_PATH = 'app/media/default.png'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
