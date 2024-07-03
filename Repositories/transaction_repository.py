from repositories.functions import sql_request_save, sql_request_fetcone, sql_request_fetchall
from models import *

class transaction_repository:

    def get_user_id_by_phone(self, phone_number: int) -> int:
        result = sql_request_fetcone("SELECT user_id FROM user WHERE phone_number = ?", (phone_number,))
        if result:
            return result[0]
        else:
            print(f"User with phone number {phone_number} not found")
            return None
        
    def add_income(self, amount: float, phone_number: str, date: str, description: str, category: int) -> bool:
        return self.add_transaction(amount, phone_number, date, description, 1, category)

    def add_expense(self, amount: float, phone_number: str, date: str, description: str, category: int) -> bool:
        return self.add_transaction(amount, phone_number, date, description, 0, category)
    

    def add_transaction(self, amount: float, phone_number: str, date: str, description: str, transaction_type: int, category: int) -> bool:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:
            
            return sql_request_save(
                "INSERT INTO user_transaction (amount, user_id, date, description, type, category_id) VALUES (?, ?, ?, ?, ?, ?)",
                (amount, user_id, date, description, transaction_type, category)
            )
        return False

    def check_balance(self, phone_number: int) -> int:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:
            user_transaction = sql_request_fetchall("SELECT amount, type FROM user_transaction WHERE user_id = ?", (user_id,))

            zero_list = [item for item in user_transaction if item[1] == 0]
            one_list = [item for item in user_transaction if item[1] == 1]

            sum_zero = sum(item[0] for item in zero_list)
            sum_one = sum(item[0] for item in one_list)

            total_sum = sum_one - sum_zero
            return total_sum
        else:
            return 0

    def history_transaction(self, phone_number: int) -> bool | tuple[None, None]:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:
            history = sql_request_fetchall(
                "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ?", 
                                        (user_id,))
            return history
        else:
            return None, None

    def sorting_by_date(self, phone_number: int) -> bool | tuple[None, None]:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:
            sorted_by_date = sql_request_fetchall(
                "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? ORDER BY date", 
                                                        (user_id,))
            return sorted_by_date
        else:
            return None, None

    def sorting_by_type(self, phone_number: int) -> bool | tuple[None, None]:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:
                
                incoming_sorted_type = sql_request_fetchall(
                    "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? AND type = ?", (user_id, 1))

                outgoing_sorted_type = sql_request_fetchall(
                    "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? AND type = ?", (user_id, 0))
                
                if incoming_sorted_type or outgoing_sorted_type:
                    return incoming_sorted_type, outgoing_sorted_type
                else:
                    return False
        else:
            return None, None

    def filter_by_category(self, phone_number: int, category_id: int) -> bool | tuple[None, None]:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:
            incoming_filter_category = sql_request_fetchall(
                "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? AND type = ? AND category_id = ?", 
                            (user_id, 1, category_id))

            outgoing_filter_category = sql_request_fetchall(
                "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? AND type = ? AND category_id = ?", 
                            (user_id, 0, category_id))

            if outgoing_filter_category or incoming_filter_category:
                return outgoing_filter_category, incoming_filter_category
            else:
                return False
        else:
            return False

    def filter_by_type(self, phone_number: int) -> bool | tuple[None, None]:
        user_id = self.get_user_id_by_phone(phone_number)
        if user_id is not None:

            incoming_filter_type = sql_request_fetchall(
                "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? AND type = ?", 
                            (user_id, 1))

            outgoing_filter_type = sql_request_fetchall(
                "SELECT amount, date, description, type, category_id FROM user_transaction WHERE user_id = ? AND type = ?", 
                            (user_id, 0))
            
            if outgoing_filter_type or incoming_filter_type:
                return outgoing_filter_type, incoming_filter_type
            else:
                return False
        else:
            return False