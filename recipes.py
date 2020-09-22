import os

import requests


class Recipe:

    def __init__(self, url_get_post, api_token):
        self.url_get_post = url_get_post
        self.api_token = api_token

    def get(self):
        request = requests.get(self.url_get_post)
        recipes = request.json()
        return recipes

    def post(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.api_token}'
        }
        request = requests.post(self.url_get_post, headers=headers, json=payload)
        return request

    def patch(self, recipe_id, files):
        headers = {
            'Authorization': f'Token {self.api_token}'
        }
        url_patch = f'{self.url_get_post}{recipe_id}/'
        requests.patch(url_patch, files=files, headers=headers)

    def add_new(self, data, files):
        request = self.post(data)
        id_post_recipe = request.json()['id']
        self.patch(files, id_post_recipe)

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
