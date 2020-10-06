import os

import requests


class Recipe:

    def __init__(self, api_url, api_token=None):
        """
        Class containing functions that work on api with recipes.

        :param api_url: <string> -> url for get and post method
        :param api_token: <string> -> api token
        """
        self.api_url = api_url
        self.api_token = api_token

    def get(self):
        response = requests.get(url=self.api_url)
        return response

    def post(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.api_token}'
        }
        response = requests.post(url=self.api_url, headers=headers, json=payload)
        return response

    def patch(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.api_token}'
        }
        response = requests.patch(self.api_url, headers=headers, json=payload)
        return response

    def delete(self):
        headers = {
            'Authorization': f'Token {self.api_token}'
        }
        response = requests.delete(self.api_url, headers=headers)
        return response

    def patch_image(self, recipe_id, files):
        headers = {
            'Authorization': f'Token {self.api_token}'
        }
        patch_url = f'{self.api_url}{recipe_id}/'
        response = requests.patch(patch_url, files=files, headers=headers)
        return response

    @staticmethod
    def get_id_post(response_post):
        # a helper function for "add new()" getting the id of the added recipe
        response_data = response_post.json()
        post_id = response_data['id']
        return post_id

    def add_new(self, data, files):
        # function adding a new recipe, first add a recipe then update its picture
        response = self.post(data)
        recipe_id = self.get_id_post(response)
        self.patch_image(recipe_id, files)

    def edit(self, data, files, recipe_id):
        # function editing an existing recipe, first patch data then image if needed
        self.patch(data)
        self.patch_image(recipe_id, files)

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
