from typing import Any
from repositories.functions import sql_request_fetchall

class CategoryRepository:

    def get_category(self) -> Any | list[Any] | bool:
        categories = sql_request_fetchall("SELECT name FROM category",)
        if categories is not None:
            return categories
        else:
            print("No categories found.")