from models import *
from repositories.transaction_repository import transaction_repository
from repositories.user_repository import *

class transaction_service:
    def __init__(self):
        self.transaction_repository = transaction_repository()
    
    def add_income(self, amount, phone_number, date, description, category) -> bool:
        return self.transaction_repository.add_income(amount, phone_number, date, description, category) 
    
    def add_expense(self, amount, phone_number, date, description, category) -> bool:
        return self.transaction_repository.add_expense(amount, phone_number, date, description, category)
    
    def check_balance(self, phone_number) -> int:
        return self.transaction_repository.check_balance(phone_number)
    
    def history_transaction(self, phone_number) -> bool | tuple[None, None]:
        return self.transaction_repository.history_transaction(phone_number)

    def sorted_by_date(self, phone_number) -> bool | tuple[None, None]:
        return self.transaction_repository.sorting_by_date(phone_number)
    
    def sorted_by_type(self, phone_number) -> bool | tuple[None, None]:
        return self.transaction_repository.sorting_by_type(phone_number)
    
    def filter_by_category(self, phone_number, category) -> bool | tuple[None, None]:
        return self.transaction_repository.filter_by_category(phone_number, category)
    
    def filter_by_type(self, phone_number) -> bool | tuple[None, None]:
        return self.transaction_repository.filter_by_type(phone_number)