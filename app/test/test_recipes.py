import unittest
from unittest.mock import patch, Mock

import requests

from app import app
from forms import RecipeAddForm
from recipes import ApiHandler, RecipeFormDataHandler, RecipeManager


class TestApiHandler(unittest.TestCase):

    def setUp(self):
        self.api_handler = ApiHandler(token=None)
        self.recipe_data = {
            'id': 48,
            'ingredients': [
                {
                    'id': 50,
                    'food': {
                        'id': 10,
                        'name': 'sfsgsg',
                        'recipe': None
                    },
                    'unit': 'PIECE',
                    'amount': 6}],
            'steps': [
                {
                    'id': 48,
                    'instruction': 'Pokroi',
                    'order': 0}
            ],
            'name': 'HIHI',
            'image': 'https://recipes-cookbook-api.herokuapp.com/media/recipes_images/default.png',
            'description': 'asfasg',
            'portions': 1,
            'preparation_time': 15,
            'difficulty': 'MEDIUM',
            'rating': '0', 'date_posted': '2020-09-21T20:06:21.561247Z'
        }
        self.payload = {
            'ingredients': [
                {
                    'food': {
                        'name': 'Food name'
                    },
                    'unit': 'GRAM',
                    'amount': 5
                }
            ],
            'steps': [
                {
                    'instruction': 'Dice food'
                }
            ],
            'name': 'New recipe',
            'description': 'Nice recipe',
            'portions': 2,
            'preparation_time': 5,
            'difficulty': 'EASY'
        }
        self.form_data = {
            'name': 'New recipe',
            'description': 'Nice recipe',
            'ingredients': [
                {
                    'food': {
                        'name': 'Food name'
                    },
                    'unit': 'GRAM',
                    'amount': 5}
            ],
            'steps': [
                {'instruction': 'Dice food'}
            ],
            'portions': 1,
            'preparation_time': 5,
            'difficulty': 'EASY'
        }
        self.api_main_url = 'https://recipes-cookbook-api.herokuapp.com/api/recipes/'
        app.app_context().push()

    @patch('recipes.requests.get')
    def test_get(self, mock_get):
        recipes = [self.recipe_data]

        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipes

        response = self.api_handler.get_response(self.api_main_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipes)

    @patch('app.requests.post')
    def test_post(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = self.payload

        response = self.api_handler.post_response(self.api_main_url, self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.payload)

    @patch('recipes.requests.patch')
    def test_patch(self, mock_patch):
        mock_patch.return_value = Mock(status_code=200)
        mock_patch.return_value.json.return_value = self.payload

        response = self.api_handler.patch_response(f'{self.api_main_url}1/?author__username=test_user', self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.payload)

    @patch('recipes.requests.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)

        response = self.api_handler.delete_response(f'{self.api_main_url}1/')

        self.assertEqual(response.status_code, 200)

    @patch('recipes.requests.patch')
    def test_patch_files(self, mock_patch):
        self.recipe_form = RecipeFormDataHandler()
        form = RecipeAddForm(data=self.form_data)
        image_path = '../app/media/default.png'
        mock_patch.return_value = Mock(status_code=200)

        _, files = self.recipe_form.get_recipe_form_data(form, image_path)
        files['image'][1].close()
        response = self.api_handler.patch_files_response('patch_to_image', files)

        self.assertEqual(response.status_code, 200)


class TestRecipeFormData(unittest.TestCase):

    def setUp(self):
        self.r = RecipeFormDataHandler()
        self.form_data = {
            'name': 'New recipe',
            'description': 'Nice recipe',
            'ingredients': [
                {
                    'food': {
                        'name': 'Food name'
                    },
                    'unit': 'GRAM',
                    'amount': 5}
            ],
            'steps': [
                {'instruction': 'Dice food'}
            ],
            'portions': 1,
            'preparation_time': 5,
            'difficulty': 'EASY'
        }

    def test_get_form_data(self):
        form = RecipeAddForm(data=self.form_data)
        image_path = '../app/media/default.png'

        payload, files = self.r.get_recipe_form_data(form, image_path)
        files['image'][1].close()

        self.assertEqual(payload, self.form_data)
        self.assertEqual(files['image'][0], 'default.png')


class TestRecipeManager(unittest.TestCase):

    def setUp(self):
        self.recipe_manager = RecipeManager(api_token=None)
        self.recipe_data = {
            'id': 48,
            'ingredients': [
                {
                    'id': 50,
                    'food': {
                        'id': 10,
                        'name': 'sfsgsg',
                        'recipe': None
                    },
                    'unit': 'PIECE',
                    'amount': 6}],
            'steps': [
                {
                    'id': 48,
                    'instruction': 'Pokroi',
                    'order': 0}
            ],
            'name': 'HIHI',
            'image': 'https://recipes-cookbook-api.herokuapp.com/media/recipes_images/default.png',
            'description': 'asfasg',
            'portions': 1,
            'preparation_time': 15,
            'difficulty': 'MEDIUM',
            'rating': '0', 'date_posted': '2020-09-21T20:06:21.561247Z'
        }
        self.form_data = {
            'name': 'New recipe',
            'description': 'Nice recipe',
            'ingredients': [
                {
                    'food': {
                        'name': 'Food name'
                    },
                    'unit': 'GRAM',
                    'amount': 5}
            ],
            'steps': [
                {'instruction': 'Dice food'}
            ],
            'portions': 1,
            'preparation_time': 5,
            'difficulty': 'EASY'
        }
        self.payload = {
            'ingredients': [
                {
                    'food': {
                        'name': 'Food name'
                    },
                    'unit': 'GRAM',
                    'amount': 5
                }
            ],
            'steps': [
                {
                    'instruction': 'Dice food'
                }
            ],
            'name': 'New recipe',
            'description': 'Nice recipe',
            'portions': 2,
            'preparation_time': 5,
            'difficulty': 'EASY'
        }

    @patch('requests.post')
    def test_posted_recipe_id(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = self.recipe_data

        response = requests.post(url='test_url')
        post_id = self.recipe_manager.posted_recipe_id(response)

        self.assertEqual(post_id, self.recipe_data['id'])

    @patch('recipes.requests.get')
    def test_get_all_recipes_response(self, mock_get):
        recipes = [self.recipe_data]
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipes

        response = self.recipe_manager.get_all_recipes_response()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipes)

    @patch('recipes.requests.get')
    def test_get_recipe_response(self, mock_get):
        recipe = self.recipe_data
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipe

        response = self.recipe_manager.get_recipe_response(48)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipe)

    @patch('recipes.requests.get')
    def test_get_user_recipe_response(self, mock_get):
        recipe = self.recipe_data
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipe

        response = self.recipe_manager.get_user_recipe_response('test_user', 48)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipe)

    @patch('recipes.requests.get')
    def test_get_user_recipes_response(self, mock_get):
        recipes = [self.recipe_data]
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipes

        response = self.recipe_manager.get_user_recipes_response('test_user')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipes)

    @patch('recipes.requests.post')
    @patch('recipes.requests.patch')
    def test_add(self, mock_post, mock_patch):
        form = RecipeAddForm(data=self.form_data)
        self.recipe_form = RecipeFormDataHandler()
        image_path = '../app/media/default.png'
        mock_post.return_value.json.return_value = self.recipe_data
        mock_patch.return_value = Mock(status_code=200)
        mock_post.return_value = Mock(status_code=200)

        data, files = self.recipe_form.get_recipe_form_data(form, image_path)
        files['image'][1].close()

        response_post, response_patch = self.recipe_manager.add(data=data, files=files)

        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(response_patch.status_code, 200)

    @patch('recipes.requests.patch')
    def test_edit(self, mock_patch):
        form = RecipeAddForm(data=self.form_data)
        self.recipe_form = RecipeFormDataHandler()
        image_path = '../app/media/default.png'
        mock_patch.return_value = Mock(status_code=200)

        data, files = self.recipe_form.get_recipe_form_data(form, image_path)
        files['image'][1].close()

        response_patch_recipe, response_patch_image = self.recipe_manager.edit(data=self.payload, files=files, pk=1,
                                                                               username='test_user')

        self.assertEqual(response_patch_recipe.status_code, 200)
        self.assertEqual(response_patch_image.status_code, 200)

    @patch('recipes.requests.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)

        response = self.recipe_manager.delete(pk=1, username='test_user')

        self.assertEqual(response.status_code, 200)

    def test_get_form_data(self):
        form = RecipeAddForm(data=self.form_data)
        image_path = '../app/media/default.png'

        payload, files = self.recipe_manager.get_form_data(form, image_path)
        files['image'][1].close()

        self.assertEqual(payload, self.form_data)
        self.assertEqual(files['image'][0], 'default.png')


if __name__ == "__main__":
    unittest.main()
