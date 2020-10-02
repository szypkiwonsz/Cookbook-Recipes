import os

import requests


class Recipe:

    def __init__(self, url_get_post, api_token=None):
        """
        Class containing functions that work on api with recipes.

        :param url_get_post: <string> -> url for get and post method
        :param api_token: <string> -> api token
        """
        self.url_get_post = url_get_post
        self.api_token = api_token

    def get(self):
        response = requests.get(self.url_get_post)
        return response

    def post(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.api_token}'
        }
        response = requests.post(self.url_get_post, headers=headers, json=payload)
        return response

    def patch_image(self, recipe_id, files):
        headers = {
            'Authorization': f'Token {self.api_token}'
        }
        url_patch = f'{self.url_get_post}{recipe_id}/'
        response = requests.patch(url_patch, files=files, headers=headers)
        return response

    @staticmethod
    def get_id_post(response_post):
        """A helper function for "patch_image()" getting the id of the added recipe."""
        id_post = response_post.json()['id']
        return id_post

    def add_new(self, data, files):
        """Function adding a new recipe, first add a recipe then update its picture."""
        response = self.post(data)
        id_post_recipe = self.get_id_post(response)
        self.patch_image(id_post_recipe, files)

    @staticmethod
    def get_form_data(form, image_path):
        payload = {
            'ingredients': [ingredient for ingredient in form.ingredients.data],
            "steps": [step for step in form.steps.data],
            'name': form.name.data,
            'description': form.description.data,
            'portions': form.portions.data,
            'preparation_time': form.preparation_time.data,
            'difficulty': form.difficulty.data
        }
        files = {
            'image': (os.path.basename(image_path), open(image_path, 'rb'), 'application/octet-stream')
        }
        return payload, files
