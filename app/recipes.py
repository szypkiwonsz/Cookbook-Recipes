import os

import requests


class RecipeManager:
    """Contains the most important methods for managing recipe."""

    def __init__(self, api_token=None):
        """
        :param api_token: <str> -> api token
        """
        self.api_main_url = 'https://recipes-cookbook-api.herokuapp.com/api/recipes/'
        self.recipe_api_handler = ApiHandler(token=api_token)
        self.recipe_form_data_handler = RecipeFormDataHandler()

    def get_all_recipes_response(self):
        """Gets all recipes from API as response.
        :return: <requests.models.Response> -> api response
        """
        return self.recipe_api_handler.get_response(self.api_main_url)

    def get_recipe_response(self, pk):
        """
        Gets one selected from API as response.
        :param pk: <int> -> recipe pk
        :return: <requests.models.Response> -> api response
        """
        return self.recipe_api_handler.get_response(f'{self.api_main_url}{pk}/')

    def get_user_recipe_response(self, username, pk):
        """
        Gets selected user recipe as response.
        :param username: <str> -> user username
        :param pk: <int> -> recipe pk
        :return: <requests.models.Response> -> api response
        """
        return self.recipe_api_handler.get_response(f'{self.api_main_url}{pk}/?author__username={username}')

    def get_user_recipes_response(self, username):
        """
        Gets all user recipes as response.
        :param username: <str> -> user username
        :return: <requests.models.Response> -> api response
        """
        return self.recipe_api_handler.get_response(f'{self.api_main_url}?author__username={username}')

    @staticmethod
    def posted_recipe_id(response_of_posted_recipe):
        """
        Helper function for "add new()" getting the id of the added recipe.
        :param response_of_posted_recipe: <requests.models.Response> -> api response of posted recipe
        :return: <int> -> id of posted recipe
        """
        response_data = response_of_posted_recipe.json()
        posted_recipe_id = response_data.get('id', None)
        return posted_recipe_id

    def add(self, data, files):
        """
        Adds a new recipe, first add a recipe then update its picture.
        :param data: <dict> -> recipe data to be uploaded
        :param files: <dict> -> recipe files (image) to be uploaded
        :return: <requests.models.Response>, <requests.models.Response> -> recipe post response, image patch response
        """
        post_recipe_response = self.recipe_api_handler.post_response(self.api_main_url, data)
        recipe_id = self.posted_recipe_id(post_recipe_response)
        patch_url = f'{self.api_main_url}{recipe_id}/'
        patch_image_response = self.recipe_api_handler.patch_files_response(url=patch_url, files=files)
        return post_recipe_response, patch_image_response

    def edit(self, data, files, pk, username):
        """
        Edits an existing recipe, first patch data then image if needed.
        :param data: <dict> -> recipe data to be uploaded
        :param files: <dict> -> recipe files (image) to be uploaded
        :param pk: <int> -> recipe pk
        :param username: <str> -> user username
        :return: <requests.models.Response>, <requests.models.Response> -> recipe post response, image patch response
        """
        post_recipe_response = self.recipe_api_handler.patch_response(
            url=f'{self.api_main_url}{pk}/?author__username={username}', payload=data)
        patch_url = f'{self.api_main_url}{pk}/'
        patch_image_response = self.recipe_api_handler.patch_files_response(url=patch_url, files=files)
        return post_recipe_response, patch_image_response

    def delete(self, pk, username):
        """
        Deletes an existing recipe.
        :param pk: <int> -> recipe pk
        :param username: <str> -> user username
        :return: <requests.models.Response> -> recipe delete response
        """
        return self.recipe_api_handler.delete_response(
            url=f'{self.api_main_url}{pk}/?author__username={username}')

    def get_form_data(self, form, image_patch):
        """

        :param form: <forms.RecipeAddForm> -> recipe add form
        :param image_patch: <str> -> image path of uploaded image
        :return: <dict>, <dict> -> recipe data, recipe files (image) data
        """
        return self.recipe_form_data_handler.get_recipe_form_data(form=form, image_path=image_patch)


class RecipeFormDataHandler:
    """Class dealing with extracting data from the add recipe form."""

    @staticmethod
    def get_recipe_form_data(form, image_path):
        """
        Gets recipe data from form needed to load into api.
        :param form: <forms.RecipeAddForm> -> recipe add form
        :param image_path: <str> -> path to uploaded recipe image
        :return: <dict>, <dict> -> recipe data, recipe files (image) data
        """
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
        else:  # for edit page
            files = None  # if the file path does not exist, leave the current image
        return payload, files


class ApiHandler:
    """Class containing functions that work on api."""

    def __init__(self, token=None):
        """
        :param token: <string> -> api token
        """
        self.token = token

    @staticmethod
    def get_response(url):
        """
        Gets recipe response
        :param url: <str> -> api url
        :return: <requests.models.Response> -> api response
        """
        response = requests.get(url=url)
        return response

    def post_response(self, url, payload):
        """
        Gets post response
        :param url: <str> -> api url
        :param payload: <dict> -> data to be uploaded
        :return: <requests.models.Response> -> api response
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.token}'
        }
        response = requests.post(url=url, headers=headers, json=payload)
        return response

    def patch_response(self, url, payload):
        """
        Gets patch response
        :param url: <str> -> api url
        :param payload: <dict> -> data to be uploaded
        :return: <requests.models.Response> -> api response
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.token}'
        }
        response = requests.patch(url, headers=headers, json=payload)
        return response

    def delete_response(self, url):
        """
        Gets delete response
        :param url: <str> -> api url
        :return: <requests.models.Response> -> api response
        """
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = requests.delete(url, headers=headers)
        return response

    def patch_files_response(self, url, files):
        """
        Gets patched files response
        :param url: <str> -> api url
        :param files: <dict> -> files to be patched
        :return: <requests.models.Response> -> api response
        """
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = requests.patch(url, files=files, headers=headers)
        return response
