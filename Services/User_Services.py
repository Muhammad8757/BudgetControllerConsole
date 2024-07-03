from models import *
from repositories.user_repository import user_repository
from repositories.user_repository import *



class user_service:
    def __init__(self):
        self.user_repository = user_repository()

    def create_user(self, user: user) -> bool:
        return self.user_repository.create_user(user)
        
    def check_user(self, phone_number, password) -> bool:
        if(self.user_repository.check_user(phone_number, password)):
            return True
        else:
            return False

    def get_user(self, phone_user, password) -> user:
        user = self.user_repository.get_user(phone_user, password)
        return user

    def update_user(self, phone_number, password, update_password) -> bool:
        if self.user_repository.update_user(phone_number, password, update_password):
            return True
        else:
            return False

    def delete_user(self, phone_user, password) -> bool:
        if self.user_repository.delete_user(phone_user, password):
            return True
        else:
            return False