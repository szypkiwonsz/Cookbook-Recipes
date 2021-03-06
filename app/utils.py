import os

from flask_paginate import Pagination, get_page_args

from config import DEFAULT_RECIPE_IMAGE_PATH


class Paginate:
    """Data pagination class."""

    def __init__(self, data, css_framework):
        """
        :param data: <list> -> data to be paginated
        :param css_framework: <string> -> name of css framework e.g. "bootstrap4"
        """
        self.data = data
        self.page, self.per_page, self.offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        self.total = len(data)
        self.css_framework = css_framework

    def get_data(self, offset=0, per_page=10):
        return self.data[offset: offset + per_page]

    def pagination(self):
        return Pagination(page=self.page, per_page=self.per_page, total=self.total, css_framework=self.css_framework)


def delete_image_file(image_file, image_path):
    """Deletes image file from local storage."""
    image_file.close()
    if image_path != DEFAULT_RECIPE_IMAGE_PATH:
        os.remove(image_path)
