import unittest
from unittest.mock import patch

from flask import g
from flask_testing import TestCase

from app import app


class TestRecipesRoutes(TestCase):

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
        pass

    def test_recipe_add_url_not_logged(self):
        response = self.client.get('/recipes/add/')
        self.assertEqual(response.status_code, 302)
        # self.assert_template_used('login.html')
        # self.assert_context()

    def test_recipe_add_url(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_token'] = 'test_token'
                session['username'] = 'test_user'
            response = c.get('/recipes/add/')
            self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('login.html')

    def test_logout_url(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('logout.html')

    def test_register_url(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('register.html')

    def test_recipe_edit_url(self):
        pass

    def test_recipe_delete_url(self):
        pass

    def test_recipe_detail_url(self):
        pass


if __name__ == "__main__":
    unittest.main()
