import unittest

from flask_testing import TestCase

from config import app
from forms import RecipeAddForm, LoginForm


class TestRecipeForms(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        return app

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

    def test_login_form(self):
        form = LoginForm(data={
            'username': 'username',
            'password': 'password'
        })
        self.assertTrue(form.validate())

    def test_login_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.validate())
        self.assertEqual(len(form.errors), 2)


if __name__ == "__main__":
    unittest.main()
