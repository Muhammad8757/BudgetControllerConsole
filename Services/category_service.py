from typing import Any
from models import *
from repositories.category_repository import CategoryRepository
from repositories.user_repository import *

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get(self) -> Any | list[Any] | bool:
        return self.repository.get_category()
