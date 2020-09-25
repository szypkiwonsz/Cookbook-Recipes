import unittest

from flask_testing import TestCase

from app.app import app


class TestRecipesRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_recipe_list_url(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('recipe_list.html')
        # self.assert_context()

    def test_recipe_add_url(self):
        response = self.client.get('recipes/add/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('recipe_add.html')
        # self.assert_context()


if __name__ == "__main__":
    unittest.main()
