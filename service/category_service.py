from typing import Any
from model import *
from repository.category_repository import CategoryRepository
from repository.user_repository import *

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get(self) -> Any | list[Any] | bool:
        return self.repository.get_category()
