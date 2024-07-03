import sqlite3
from main_functions import *
from enum import Enum

from menus import login_menu, main_menu


class cmd(Enum):
    cmd_1 = 1
    cmd_2 = 2
    cmd_3 = 3

class cmd_choose(Enum):
    cmd_1 = 1
    cmd_2 = 2 
    cmd_3 = 3 
    cmd_4 = 4 
    cmd_5 = 5 
    cmd_6 = 6 
    cmd_7 = 7 
    cmd_8 = 8 
    cmd_9 = 9
    cmd_10 = 10
    cmd_11 = 11
    cmd_12 = 12
    cmd_0 = 0

def register_user():
    name = input("Введите имя: ")
    phone_number = input("Введите телефонный номер: ")
    password = input("Введите пароль: ")
    user = user(name, phone_number, password)
    if service.CreateUser(user):
        print("Пользователь успешно зарегистрирован")
        login_user(phone_number, password)
    else:
        print("Пользователь с таким номером уже зарегистрирован или произошла ошибка при регистрации")
        return

def login_user(phone_number=None, password=None):
    print_separator()
    if not phone_number:
        phone_number = input("Введите телефонный номер: ")
    while True:
        if not password:
            password = input("Введите пароль: ")
        if service.check_user(phone_number, password):
            print("Авторизация прошла успешно")
            print_separator()
            program(phone_number, password)
        else:
            print("Неправильный пароль. Повторите попытку.")
            retry = int(input("Хотите попробовать снова? (да - 1 / нет - 0): "))
            if retry == 1:
                phone_number = input("Введите телефонный номер: ")
                password = input("Введите пароль: ")
            else:
                print("Выход из программы")
                break

def program(phone_number=None, password=None):
    while True:
        login_menu()
        print_separator()
        cmd_login = int(input("> "))
        print_separator()
        if cmd_login == cmd_choose.cmd_1.value: 
            cmd_1(phone_number, password) #получения данных о пользователе
        elif cmd_login == cmd_choose.cmd_2.value: 
            cmd_2(phone_number, password) #обновления пароля пользователя
            break
        elif cmd_login == cmd_choose.cmd_3.value: 
            cmd_3(phone_number, password) #удаления пользователя
        elif cmd_login == cmd_choose.cmd_4.value: #вывод вссех категорий
            print_category()
            print_separator()
        elif cmd_login == cmd_choose.cmd_5.value: 
            cmd_5(phone_number) # добавить новый расход
        elif cmd_login == cmd_choose.cmd_6.value: 
            cmd_6(phone_number) #добавить новый доход
        elif cmd_login == cmd_choose.cmd_7.value: #вывод сумму пользователя
            delimiter(1)
            print(f"Сумма пользователя: {transaction_service.check_balance(phone_number)}")
            delimiter(1)
            print_separator()
        elif cmd_login == cmd_choose.cmd_8.value: #вывод истории 
            res_history = transaction_service.history_transaction(phone_number)
            print_history_filter(res_history)
            print_separator()
        elif cmd_login == cmd_choose.cmd_9.value: #сортировка по дате
            res_date = transaction_service.sorted_by_date(phone_number)
            print_history_filter(res_date)
            print_separator()
        elif cmd_login == cmd_choose.cmd_10.value: 
            cmd_10(phone_number) #сортировка по типу (доход или расход)
        elif cmd_login == cmd_choose.cmd_11.value: 
            cmd_11(phone_number) #фильтр по категории
        elif cmd_login == cmd_choose.cmd_12.value:
            cmd_12(phone_number) #фильтр по типу
        elif cmd_login == cmd_choose.cmd_0.value:
            break
        else:
            print("Неверная команда. Повторите попытку")


def main() -> None:
    while True:
        try:
            main_menu()
            cmd_input = int(input("> "))
            if cmd_input == cmd.cmd_1.value:
                register_user()
            elif cmd_input == cmd.cmd_2.value:
                login_user()
            elif cmd_input == cmd.cmd_3.value:
                print("Выход из программы")
                break
            else:
                print("Неверная команда. Повторите попытку")
        except sqlite3.Error as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":  
    main()