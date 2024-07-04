from datetime import *
from enum import Enum
from model import transaction_details
from model.models import user
from service.user_services import UserService
from service.category_service import CategoryService
from service.transaction_service import TransactionService
from menus import delimiter, login_menu

service = UserService()
category_service = CategoryService()
transaction_service = TransactionService()


class Commands(Enum):
    """
    Перечисление команд для основного меню.
    """
    register_user = 1
    login_user = 2
    exit = 0

class CommandChoice(Enum):
    """
    Перечисление команд для меню пользователя.
    """
    get_user = 1
    update_password = 2 
    delete_user = 3 
    get_category = 4 
    add_expense = 5 
    add_income = 6 
    check_balance = 7 
    get_history = 8 
    sorted_by_date = 9
    sorted_by_type = 10
    filter_by_category = 11
    filter_by_type = 12
    exit = 0





def register_user():
    """
    Функция для регистрации нового пользователя.
    
    Запрашивает имя, телефонный номер и пароль, создает пользователя и
    сохраняет его в базе данных.
    """
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


class View:
    """
    Класс для отображения данных и взаимодействия с пользователем.
    """
    
    def print_separator(self):
        """
        Отображает разделитель.
        """
        print("\t")

    def print_category(self):
        """
        Отображает все категории.
        """
        category = category_service.get()
        k = 1
        delimiter(1)
        while k-1 < len(category): 
            for i in category:
                print(f"{k}. {i[0]}")
                k += 1
            delimiter(1)

    def category_mean(self, int) -> str:
        """
        Возвращает название категории по ее номеру.
        """
        category = category_service.get()
        k = 1
        while k-1 < len(category): 
            for i in category:
                if k == int:
                    return i[0]
                k += 1

    def print_history_filter(self, res):
        """
        Отображает историю или фильтрованные транзакции.
        """
        if res:
            for transaction in res:
                amount = transaction[0]
                date = transaction[1]
                description = transaction[2]
                category = transaction[4]
                type_transaction = "Доход" if transaction[3] == 1 else "Расход"
                
                delimiter(1)
                print(f"Сумма:      {amount}")
                print(f"Дата:       {date}")
                print(f"Описание:   {description}")
                print(f"Категория:  {self.category_mean(category)}")
                print(f"Тип:        {type_transaction}")
        else:
            print("Ничего не найдено")

    def print_transaction(self, index, res):
        """
        Отображает транзакцию по индексу.
        """
        if res:
            for transaction in res[index]:
                amount = transaction[0]
                date = transaction[1]
                description = transaction[2]
                category = transaction[4]
                type_transaction = "Доход" if transaction[3] == 1 else "Расход"
                
                delimiter(1)
                print(f"Сумма:      {amount}")
                print(f"Дата:       {date}")
                print(f"Описание:   {description}")
                print(f"Категория:  {self.category_mean(category)}")
                print(f"Тип:        {type_transaction}")
        else:
            print("Ничего не найдено")
        
    def get_transaction_details(self) -> transaction_details:
        """
        Возвращает детали транзакции, введенные пользователем.
        
        Возвращает:
        transaction_details: Объект с деталями транзакции.
        """
        while True:
            try:
                amount = float(input("Введите сумму: "))
                if amount < 0:
                    print("Введите сумму больше 0")
                    continue
            except ValueError:
                print("Введите числовое значение для суммы")
                continue

            description = input("Введите описание (или оставьте пустым): ")
            self.print_category()
            category = input("Введите категорию (или оставьте пустым): ")

            if category:
                try:
                    category_id = int(category)
                    if category_id < 1 or category_id > len(category_service.get()):
                        print("Введите правильную категорию")
                        continue
                except ValueError:
                    print("Введите числовое значение для категории")
                    continue
            else:
                category_id = None

            date = datetime.now().replace(second=0, microsecond=0)
            transaction_details_info = transaction_details(amount, date, description, category_id)
            return transaction_details_info

    def get_user(self, phone_number, password):
        """
        Отображает данные о пользователе.
        """
        user = service.get_user(phone_number, password)
        if user is not None:
            self.print_separator()
            delimiter(1)
            print(f"Имя пользователя:  {user[0]}")
            print(f"Номер телефона:    {user[1]}")
            
            delimiter(1)
            self.print_separator()
        else:
            print("Пользователь не найден")

    def update_password(self, phone_number, password):
        """
        Обновляет пароль пользователя.
        """
        new_password = input("Введите новый пароль: ")
        confirm_password = input("Введите старый для подверждения: ")
        if confirm_password == password:
            if service.update_user(phone_number, password, new_password):
                print("Пароль успешно обновлен")

                # Отложенный импорт для предотвращения циклического импорта
                from main import program

                program(phone_number, new_password)
        else:
            print("Произошла ошибка. Повторите попытку")

    def delete_user(self, phone_number, password) -> bool:
        """
        Удаляет пользователя.
        """
        confirm_password = input("Введите пароль для подверждения: ")
        confirm_delete = input("Вы уверены, что хотите удалить пользователя? (да - 1/нет - 0): ")
        if confirm_delete.lower() == '1':
            if confirm_password == password:
                if service.delete_user(phone_number, password):
                    print("Пользователь успешно удален")
                    return True
            else:
                print("Произошла ошибка при удалении пользователя")
                return False
        else:
            print("Удаление отменено")
            return False

    def add_expense(self, phone_number):
        """
        Добавляет новый расход.
        """
        details = self.get_transaction_details()
        if details:
            amount, date, description, category = details.amount, details.date, details.description, details.category_id
            if transaction_service.add_expense(amount, phone_number, date, description, category):
                self.print_separator()
                print("Расход успешно добавлен")
                self.print_separator()
            else:
                print("Произошла ошибка")

    def add_income(self, phone_number):
        """
        Добавляет новый доход.
        """
        details = self.get_transaction_details()
        if details:
            amount, date, description, category = details.amount, details.date, details.description, details.category_id
            if transaction_service.add_income(amount, phone_number, date, description, category):
                self.print_separator()
                print("Доход успешно добавлен")
                self.print_separator()
            else:
                print("Произошла ошибка")

    def sorted_by_type(self, phone_number):
        """
        Сортирует транзакции по типу (доход или расход).
        """
        res_type = transaction_service.sorted_by_type(phone_number)
        if res_type:
            type_sort_int = int(input(f"1. Сортировка по Доходу\n0. Сортировка по Расход\n> "))
            if type_sort_int == 1:
                self.print_transaction(0, res_type) # income 0
                self.print_transaction(1, res_type) # expense 1
            else:
                self.print_transaction(1, res_type)
                self.print_transaction(0, res_type)
        else:
            print("Ничего не найдено")

    def filter_by_category(self, phone_number):
        """
        Фильтрует транзакции по категории.
        """
        self.print_category()
        category = int(input("Введите категорию: "))
        res_category = transaction_service.filter_by_category(phone_number, category)
        if res_category is False:
            self.print_separator()
            print("Ничего не найдено")
            self.print_separator()
        else:
            self.print_transaction(0, res_category)
            self.print_transaction(1, res_category)
            self.print_separator()

    def filter_by_type(self, phone_number):
        """
        Фильтрует транзакции по типу.
        """
        type_int = int(input("Введите тип (например: 1 - (Доход) или 0 - (Расход)): "))
        self.print_separator()
        if type_int > 1 or type_int < 0:
            self.print_separator()
            print("Введите правильный тип")
            self.print_separator()
        else:
            res_type = transaction_service.filter_by_type(phone_number)
            if res_type is False:
                self.print_separator()
                print("Ничего не найдено")
                self.print_separator()
            else:
                if type_int == 1:
                    self.print_transaction(1, res_type)
                else:
                    self.print_transaction(0, res_type)
                self.print_separator()

view = View()

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