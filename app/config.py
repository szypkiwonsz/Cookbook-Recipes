import os

from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads
# from celery import Celery

# Configuration of app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOADED_IMAGES_DEST'] = 'app/media/recipe_images'

# Configuration of images
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(app)
