import os

import requests


class Recipe:

    def __init__(self, api_url, api_token=None):
        """
        Contains the most important methods for managing recipe.

        :param api_url: <string> -> api url
        :param api_token: <string> -> api token
        """
        self.api = RecipeApi(url=api_url, token=api_token)
        self.form = RecipeFormData()

    def get(self):
        return self.api.get_recipe()

    def add(self, data, files):
        # function adding a new recipe, first add a recipe then update its picture
        response_post_recipe = self.api.post_recipe(data)
        recipe_id = self.api.posted_recipe_id(response_post_recipe)
        patch_url = f'{self.api.url}{recipe_id}/'
        response_patch_image = self.api.patch_recipe_image(patch_url=patch_url, files=files)
        return response_post_recipe, response_patch_image

    def edit(self, data, files):
        # function editing an existing recipe, first patch data then image if needed
        response_patch_recipe = self.api.patch_recipe(data)
        patch_url = self.api.url
        response_patch_image = self.api.patch_recipe_image(patch_url=patch_url, files=files)
        return response_patch_recipe, response_patch_image

    def delete(self):
        return self.api.delete_recipe()

    def get_form_data(self, form, image_patch):
        return self.form.get_recipe_form_data(form=form, image_path=image_patch)


class RecipeFormData:
    """
    Class dealing with extracting data from the add recipe form.
    """
    @staticmethod
    def get_recipe_form_data(form, image_path):
        payload = {
            'ingredients': [ingredient for ingredient in form.ingredients.data],
            "steps": [step for step in form.steps.data],
            'name': form.name.data,
            'description': form.description.data,
            'portions': form.portions.data,
            'preparation_time': form.preparation_time.data,
            'difficulty': form.difficulty.data
        }
        if image_path:
            files = {
                'image': (os.path.basename(image_path), open(image_path, 'rb'), 'application/octet-stream')
            }
        else:
            # for edit page -> if the file path does not exist, leave the current image
            files = None
        return payload, files


class RecipeApi:

    def __init__(self, url, token):
        """
        Class containing functions that work on api with recipes.

        :param url: <string> -> api url
        :param token: <string> -> api token
        """
        self.url = url
        self.token = token

    def get_recipe(self):
        response = requests.get(url=self.url)
        return response

    @staticmethod
    def posted_recipe_id(response_post):
        # a helper function for "add new()" getting the id of the added recipe
        response_data = response_post.json()
        posted_recipe_id = response_data.get('id', None)
        return posted_recipe_id

    def post_recipe(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.token}'
        }
        response = requests.post(url=self.url, headers=headers, json=payload)
        return response

    def patch_recipe(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.token}'
        }
        response = requests.patch(self.url, headers=headers, json=payload)
        return response

    def delete_recipe(self):
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = requests.delete(self.url, headers=headers)
        return response

    def patch_recipe_image(self, patch_url, files):
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = requests.patch(patch_url, files=files, headers=headers)
        return response
