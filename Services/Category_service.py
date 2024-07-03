from typing import Any
from models import *
from repositories.category_repository import category_repository
from repositories.user_repository import *

class category_service:
    def __init__(self):
        self.repository = category_repository()
    
    def get(self) -> Any | list[Any] | bool:
        return self.repository.get_category()