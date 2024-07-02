import hashlib
import sqlite3
from Models import User
from Repositories.Functions import sql_request_save, sql_request_fetcone
from Models import User

class UserRepository:
    def create_user(self, user: User):
        hash_password = hasher(user.password)
        if sql_request_save("INSERT INTO user (name, phone_number, password) VALUES (?, ?, ?)", 
                            (user.name, user.phone_number, hash_password)) is not None:
            return True
        return False

    def check_user(self, phone_user: int, password: str) -> bool:
        hash_password = hasher(password)
        return sql_request_fetcone("SELECT * FROM user WHERE phone_number = ? AND password = ?", (phone_user, hash_password))
    
    def get_user(self, phone_user: int, password: str) -> User:
        hash_password = hasher(password)
        user = sql_request_fetcone("SELECT name, phone_number FROM user WHERE phone_number = ? AND password = ?", (phone_user, hash_password))
        if user is not None:
            return (user[0], user[1])
        else:
            return None

    def update_user(self, phone_user: int, password: str, update_password: str) -> bool:
        hash_old_password = hasher(password)
        hash_new_password = hasher(update_password)
        if UserRepository.check_user(self, phone_user, password):
            if sql_request_save("UPDATE user SET password = ? WHERE phone_number = ? AND password = ? ", 
                (hash_new_password, phone_user, hash_old_password )) != 0:
                return True
            else:
                return False

    def delete_user(self, phone_user: int, password: str) -> bool:
        hash_password = hasher(password)
        if UserRepository.check_user(self, phone_user, password):
            if sql_request_save("DELETE FROM user WHERE phone_number = ? AND password = ? ", (phone_user, hash_password)) != 0:
                return True
            else:
                return False

def hasher(password):
    if isinstance(password, int):
        # Если password является числом, преобразуйте его в строку
        password = str(password)
    password_bytes = password.encode()
    hash = hashlib.md5(password_bytes)
    return hash.hexdigest()