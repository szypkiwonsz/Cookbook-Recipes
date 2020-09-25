import unittest
from unittest.mock import patch, Mock

from recipes import *


class TestRecipeClass(unittest.TestCase):

    def setUp(self):
        self.recipe = Recipe(url_get_post='https://recipes-cookbook-api.herokuapp.com/api/recipes/',
                             api_token='7863a78eadb90301bb98c7d4d06cbe497d92b756')

    def test_get(self):
        mock_get_patcher = patch('recipes.requests.get')
        recipes = [
            {
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
        ]

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = recipes

        response = self.recipe.get()

        mock_get_patcher.stop()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), recipes)

    def test_post(self):
        mock_post_patcher = patch('recipes.requests.post')
        payload = {
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

        mock_post = mock_post_patcher.start()
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = payload

        response = self.recipe.post(payload)

        mock_post_patcher.stop()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), payload)

    def test_get_id_post(self):
        pass

    def test_patch(self):
        pass

    def test_add_new(self):
        pass

    def test_get_form_data(self):
        pass
