import unittest
from unittest.mock import patch, Mock

from flask_testing import TestCase

from app import app


class TestRecipesRoutes(TestCase):

    def setUp(self):
        self.recipe = {
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
            "author": {
                "id": 1,
                "username": "test_user",
                "email": "test_email@gmail.com"
            },
            'name': 'HIHI',
            'image': 'https://recipes-cookbook-api.herokuapp.com/media/recipes_images/default.png',
            'description': 'asfasg',
            'portions': 1,
            'preparation_time': 15,
            'difficulty': 'MEDIUM',
            'rating': '0', 'date_posted': '2020-09-21T20:06:21.561247Z'
        }

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        return app

    def test_recipe_list_all_url(self):
        response = self.client.get('/recipes/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('recipe_list_all.html')
        # self.assert_context()

    def test_recipe_list_user_url(self):
        response = self.client.get('/recipes/test_user/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('recipe_list_user.html')

    def test_recipe_add_url_not_logged(self):
        response = self.client.get('/recipes/add/')

        self.assertEqual(response.status_code, 302)

    def test_recipe_add_url(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'

            response = c.get('/recipes/add/')

            self.assertEqual(response.status_code, 200)
            self.assert_template_used('recipe_add.html')

    def test_login_url(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')

    def test_logout_url_not_logged(self):
        response = self.client.get('/logout/')

        self.assertEqual(response.status_code, 302)

    def test_logout_url(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'

            response = c.get('/logout/')

            self.assertEqual(response.status_code, 200)
            self.assert_template_used('logout.html')

    def test_register_url(self):
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('register.html')

    def test_recipe_edit_url_not_logged(self):
        response = self.client.get('/recipes/test_user/2/edit/')

        self.assertEqual(response.status_code, 302)

    @patch('app.requests.get')
    def test_recipe_edit_url_no_data(self, fake_get):
        fake_get.return_value = Mock(status_code=404)
        fake_get.return_value.json.return_value = []
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'

            response = c.get('/recipes/test_user/2/edit/')

            self.assertEqual(response.status_code, 404)

    @patch('app.requests.get')
    def test_recipe_edit_url(self, fake_get):
        fake_get.return_value = Mock(status_code=200)
        fake_get.return_value.json.return_value = self.recipe
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'

            response = c.get('/recipes/test_user/2/edit/')

            self.assertEqual(response.status_code, 200)
            self.assert_template_used('recipe_edit.html')

    def test_recipe_delete_url_not_logged(self):
        response = self.client.get('/recipes/test_user/2/delete/')
        self.assertEqual(response.status_code, 302)

    @patch('app.requests.get')
    def test_recipe_delete_url_no_data(self, fake_get):
        fake_get.return_value = Mock(status_code=404)
        fake_get.return_value.json.return_value = []
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'

            response = c.get('/recipes/test_user/2/delete/')

            self.assertEqual(response.status_code, 404)

    @patch('app.requests.get')
    def test_recipe_delete_url(self, fake_get):
        fake_get.return_value = Mock(status_code=200)
        fake_get.return_value.json.return_value = self.recipe
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'

            response = c.get('/recipes/test_user/2/delete/')

            self.assertEqual(response.status_code, 200)
            self.assert_template_used('recipe_delete.html')

    @patch('app.requests.get')
    def test_recipe_detail_url_no_data(self, fake_get):
        fake_get.return_value = Mock(status_code=404)
        fake_get.return_value.json.return_value = []

        response = self.client.get('/recipes/2/')

        self.assertEqual(response.status_code, 404)

    @patch('app.requests.get')
    def test_recipe_detail_url(self, fake_get):
        fake_get.return_value = Mock(status_code=200)
        fake_get.return_value.json.return_value = self.recipe

        response = self.client.get('/recipes/2/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('recipe_detail.html')

    def test_home_page_url(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home_page.html')


if __name__ == "__main__":
    unittest.main()
