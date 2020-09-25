from flask_testing import TestCase

from app.app import app
from app.forms import RecipeAddForm


class TestRecipeForms(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_recipe_add_form_valid(self):
        form = RecipeAddForm(data={
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
        })
        self.assertTrue(form.validate())

    def test_recipe_add_form_no_data(self):
        form = RecipeAddForm(data={})
        self.assertFalse(form.validate())
        self.assertEqual(len(form.errors), 7)
