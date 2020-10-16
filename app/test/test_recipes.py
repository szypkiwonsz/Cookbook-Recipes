import unittest
from unittest.mock import patch, Mock

from app import app
from forms import RecipeAddForm
from recipes import *


class TestRecipeClass(unittest.TestCase):

    def setUp(self):
        self.recipe = Recipe(api_url='https://recipes-cookbook-api.herokuapp.com/api/recipes/',
                             api_token=None)
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
        app.app_context().push()

    @patch('recipes.requests.get')
    def test_get(self, mock_get):
        recipes = [self.recipe_data]

        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipes

        response = self.recipe.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipes)

    @patch('app.requests.post')
    def test_post(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = self.payload

        response = self.recipe.post(self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.payload)

    @patch('requests.post')
    def test_get_id_post(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = self.recipe_data

        response = requests.post(url='test_url')
        post_id = self.recipe.get_id_post(response)

        self.assertEqual(post_id, self.recipe_data['id'])

    @patch('recipes.requests.patch')
    def test_patch(self, mock_patch):
        mock_patch.return_value = Mock(status_code=200)
        mock_patch.return_value.json.return_value = self.payload

        response = self.recipe.patch(self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.payload)

    def test_add_new(self):
        pass

    with app.app_context():
        def test_get_form_data(self):
            form = RecipeAddForm(data=self.form_data)
            image_path = '../app/media/default.png'

            payload, files = self.recipe.get_form_data(form, image_path)
            files['image'][1].close()

            self.assertEqual(payload, self.form_data)
            self.assertEqual(files['image'][0], 'default.png')

    @patch('recipes.requests.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)

        response = self.recipe.delete()

        self.assertEqual(response.status_code, 200)

    @patch('recipes.requests.patch')
    def test_patch_image(self, mock_patch):
        form = RecipeAddForm(data=self.form_data)
        image_path = '../app/media/default.png'
        mock_patch.return_value = Mock(status_code=200)

        _, files = self.recipe.get_form_data(form, image_path)
        files['image'][1].close()
        response = self.recipe.patch_image('patch_to_image', files)

        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        pass


if __name__ == "__main__":
    unittest.main()
