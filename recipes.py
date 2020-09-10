import requests


class Recipes:

    @staticmethod
    def get_recipes(url_get):
        request = requests.get(url_get)
        recipes = request.json()
        return recipes
