import sqlite3
from enum import Enum
from main_functions import CommandChoice, Commands, View
from menus import login_menu, main_menu
from models import user
from services.user_services import UserService
from services.category_service import CategoryService
from services.transaction_service import TransactionService
from menus import delimiter

service = UserService()
category_service = CategoryService()
transaction_service = TransactionService()

view = View()



def register_user():
    """
    Функция для регистрации нового пользователя.
    
    Запрашивает имя, телефонный номер и пароль, создает пользователя и
    сохраняет его в базе данных.
    """
    

def login_user(phone_number=None, password=None) -> bool:
    """
    Функция для авторизации пользователя.
    
    Проверяет наличие пользователя в базе данных и правильность пароля.
    
    Параметры:
    phone_number (str): Телефонный номер пользователя.
    password (str): Пароль пользователя.
    
    Возвращает:
    bool: True, если авторизация успешна, иначе False.
    """
    if service.check_user(phone_number, password):
        print("Авторизация прошла успешно")
        view.print_separator()
        return True
    else:
        return False

def program(phone_number=None, password=None):
    """
    Основная программа для авторизованного пользователя.
    
    Позволяет пользователю выполнять различные действия, такие как
    добавление доходов и расходов, проверка баланса и фильтрация транзакций.
    
    Параметры:
    phone_number (str, optional): Телефонный номер пользователя.
    password (str, optional): Пароль пользователя.
    """
    view.print_separator()
    if not phone_number:
        phone_number = input("Введите телефонный номер: ")

    while True:
        if not password:
            password = input("Введите пароль: ")
        view.print_separator()
        if login_user(phone_number, password):
            logged_in = True
            while logged_in:
                login_menu()
                view.print_separator()
                menu_choice = int(input("> "))
                view.print_separator()
                if menu_choice == CommandChoice.get_user.value: 
                    view.get_user(phone_number, password)
                elif menu_choice == CommandChoice.update_password.value: 
                    view.update_password(phone_number, password)
                    return
                elif menu_choice == CommandChoice.delete_user.value: 
                    if view.delete_user(phone_number, password):
                        logged_in = False
                        break
                    else:
                        continue
                elif menu_choice == CommandChoice.get_category.value: 
                    view.print_category()
                    view.print_separator()
                elif menu_choice == CommandChoice.add_expense.value: 
                    view.add_expense(phone_number)
                elif menu_choice == CommandChoice.add_income.value: 
                    view.add_income(phone_number)
                elif menu_choice == CommandChoice.check_balance.value: 
                    delimiter(1)
                    print(f"Сумма пользователя: {transaction_service.check_balance(phone_number)}")
                    delimiter(1)
                    view.print_separator()
                elif menu_choice == CommandChoice.get_history.value: 
                    res_history = transaction_service.history_transaction(phone_number)
                    view.print_history_filter(res_history)
                    view.print_separator()
                elif menu_choice == CommandChoice.sorted_by_date.value: 
                    res_date = transaction_service.sorted_by_date(phone_number)
                    view.print_history_filter(res_date)
                    view.print_separator()
                elif menu_choice == CommandChoice.sorted_by_type.value: 
                    view.sorted_by_type(phone_number)
                elif menu_choice == CommandChoice.filter_by_category.value: 
                    view.filter_by_category(phone_number)
                elif menu_choice == CommandChoice.filter_by_type.value:
                    view.filter_by_type(phone_number)
                elif menu_choice == CommandChoice.exit.value:
                    return
                else:
                    print("Неверная команда. Повторите попытку")
                    
        else:
            print("Неправильный пароль. Повторите попытку.")
            retry = int(input("Хотите попробовать снова? (да - 1 / нет - 0): "))
            if retry == 1:
                phone_number = input("Введите телефонный номер: ")
                password = input("Введите пароль: ")
            else:
                print("Выход из программы")
                return

def main() -> None:
    """
    Главная функция приложения.
    
    Отображает главное меню и обрабатывает команды пользователя для регистрации,
    авторизации или выхода из программы.
    """
    while True:
        try:
            main_menu()
            CommandInput = int(input("> "))
            if CommandInput == Commands.register_user.value:
                name = input("Введите имя: ")
                phone_number = input("Введите телефонный номер: ")
                password = input("Введите пароль: ")
                result_user = user(name, phone_number, password)
                if service.create_user(result_user):
                    print("Пользователь успешно зарегистрирован")
                    program(phone_number, password)  # Здесь не передаем phone_number и password
                else:
                    print("Пользователь с таким номером уже зарегистрирован или произошла ошибка при регистрации")
                    return
            elif CommandInput == Commands.login_user.value:
                program()
            elif CommandInput == Commands.exit.value:
                print("Выход из программы")
                break
            else:
                print("Неверная команда. Повторите попытку")
        except sqlite3.Error as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":  
    main()