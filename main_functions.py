from datetime import *
from main import login_user
from models import transaction_details, user
from services.user_services import user_service
from services.category_service import category_service
from services.transaction_service import transaction_service
from menus import delimiter

service = user_service()
category_service = category_service()
transaction_service = transaction_service()


def print_separator(): #табуляция
    print("\t")

def print_category(): #вывод всех категорий
    category = category_service.get()
    k = 1
    delimiter(1)
    while k-1 < len(category): 
        for i in category:
            print(f"{k}. {i[0]}")
            k += 1
        delimiter(1)

def category_mean(int): #получает значения категории (если категрория 1 то значения Жилье если 2 то Транспорт)
    category = category_service.get()
    k = 1
    while k-1 < len(category): 
        for i in category:
            if k == int:
                return i[0]
            k += 1

def print_history_filter(res): #печатает историю или фильтр
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
            print(f"Категория:  {category_mean(category)}")
            print(f"Тип:        {type_transaction}")
    else:
        print("Ниичего не найдено")

def print_transaction(index, res): #печатает транзакцию
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
            print(f"Категория:  {category_mean(category)}")
            print(f"Тип:        {type_transaction}")
    else:
        print("Ниичего не найдено")
    
def get_transaction_details() -> transaction_details: #получения транзакционных деталей (сумму, описание и категорию)
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
        print_category()
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


def cmd_1(phone_number, password): #получения данных о пользователе
    user = service.get_user(phone_number, password)
    if user is not None:
        print_separator()
        delimiter(1)
        print(f"Имя пользователя:  {user[0]}")
        print(f"Номер телефона:    {user[1]}")
        
        delimiter(1)
        print_separator()
    else:
        print("Пользователь не найден")

def cmd_2(phone_number, password):  #обновления пароля пользователя
    new_password = input("Введите новый пароль: ")
    confirm_password = input("Введите старый для подверждения: ")
    if confirm_password == password:
        if service.update_user(phone_number, password, new_password):
            print("Пароль успешно обновлен")
            login_user(phone_number, new_password)
    else:
        print("Произошла ошибка. Повторите попытку")

def cmd_3(phone_number, password): #удаления пользователя
    confirm_password = input("Введите пароль для подверждения: ")
    confirm_delete = input("Вы уверены, что хотите удалить пользователя? (да - 1/нет - 0): ")
    if confirm_delete.lower() == '1':
        if confirm_password == password:
            if service.delete_user(phone_number, password):
                print("Пользователь успешно удален")
                return 
        else:
            print("Произошла ошибка при удалении пользователя")
    else:
        print("Удаление отменено")

def cmd_5(phone_number): # добавить новый расход
    details = get_transaction_details()
    if details:
        amount, date, description, category = details.amount, details.date, details.description, details.category_id
        if transaction_service.add_expense(amount, phone_number, date, description, category):
            print_separator()
            print("Расход успешно добавлен")
            print_separator()
        else:
            print("Произошла ошибка")

def cmd_6(phone_number): #добавить новый доход
    details = get_transaction_details()
    if details:
        amount, date, description, category = details.amount, details.date, details.description, details.category_id
        if transaction_service.add_income(amount, phone_number, date, description, category):
            print_separator()
            print("Доход успешно добавлен")
            print_separator()
        else:
            print("Произошла ошибка")

def cmd_10(phone_number): #сортировка по типу (доход или расход)
    res_type = transaction_service.sorted_by_type(phone_number)
    if res_type:
        type_sort_int = int(input(f"1. Сортировка по Доходу\n0. Сортировка по Расход\n> "))
        if type_sort_int == 1:
            print_transaction(0, res_type) # income 0
            print_transaction(1, res_type) # expense 1
        else:
            print_transaction(1, res_type)
            print_transaction(0, res_type)
    else:
        print("Ничего не найдено")

def cmd_11(phone_number): #фильтр по категории
    print_category()
    category = int(input("Введите категорию: "))
    res_category = transaction_service.filter_by_category(phone_number, category)
    if res_category is False:
        print_separator()
        print("Ничего не найдено")
        print_separator()
    else:
        print_transaction(0, res_category)
        print_transaction(1, res_category)
        print_separator()

def cmd_12(phone_number): #фильтр по типу
    type_int = int(input("Введите тип (например: 1 - (Доход) или 0 - (Расход)): "))
    print_separator()
    if type_int > 1 or type_int < 0:
        print_separator()
        print("Введите правильный тип")
        print_separator()
    else:
        res_type = transaction_service.filter_by_type(phone_number)
        if res_type is False:
            print_separator()
            print("Ничего не найдено")
            print_separator()
        else:
            if type_int == 1:
                print_transaction(1, res_type)
            else:
                print_transaction(0, res_type)
            print_separator()