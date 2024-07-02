import sqlite3
from Repositories.Functions import sql_request_fetchall


class Category_Repository:

    def get_category(self):
        categories = sql_request_fetchall("SELECT name FROM category",)
        if categories is not None:
            return categories
        else:
            print("No categories found.")