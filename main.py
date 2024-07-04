import sqlite3
from main_functions import Commands, program, register_user
from menus import login_menu, main_menu

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
                register_user()
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