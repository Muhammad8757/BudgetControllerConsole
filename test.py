# import textwrap
# from Services.Transaction_service import Transaction_Service
# from main import category_mean, delimiter


# def print_income(res):
#     if res:
#         for transaction in res[0]:
#             amount = transaction[0]
#             date = transaction[1]
#             description = transaction[2]
#             category = transaction[4]
#             type_transaction = "Доход" if transaction[3] == 1 else "Расход"
            
#             formatted_description = textwrap.fill(description, width=30)
            
#             delimiter(1)
#             print(f"Сумма:      {amount}")
#             print(f"Дата:       {date}")
#             print(f"Описание:   {formatted_description}")
#             print(f"Категория:  {category_mean(category)}")
#             print(f"Тип:        {type_transaction}")
#     else:
#         print("Ниичего не найдено")


# def print_expense(res):
#     if res:
#         for transaction in res[1]:
#             amount = transaction[0]
#             date = transaction[1]
#             description = transaction[2]
#             category = transaction[4]
#             type_transaction = "Доход" if transaction[3] == 1 else "Расход"
            
#             formatted_description = textwrap.fill(description, width=30)
            
#             delimiter(1)
#             print(f"Сумма:      {amount}")
#             print(f"Дата:       {date}")
#             print(f"Описание:   {formatted_description}")
#             print(f"Категория:  {category_mean(category)}")
#             print(f"Тип:        {type_transaction}")
#     else:
#         print("Ниичего не найдено")


# def print_transaction(index, res):
#     if res:
#         for transaction in res[index]:
#             amount = transaction[0]
#             date = transaction[1]
#             description = transaction[2]
#             category = transaction[4]
#             type_transaction = "Доход" if transaction[3] == 1 else "Расход"
            
#             formatted_description = textwrap.fill(description, width=30)
            
#             delimiter(1)
#             print(f"Сумма:      {amount}")
#             print(f"Дата:       {date}")
#             print(f"Описание:   {formatted_description}")
#             print(f"Категория:  {category_mean(category)}")
#             print(f"Тип:        {type_transaction}")
#     else:
#         print("Ниичего не найдено")


# t = Transaction_Service()

# res_type = t.sorted_by_type(12345)

# # print_income(res_type)

# print_transaction(0, res_type)

from Repositories.TransactionRepository import TransactionRepository
from Repositories.Category_Repository import *



def delimiter(count):
    for i in range(count):
        print("="*40)

t = TransactionRepository()
res = t.history_transaction(12345)
c = Category_Repository()



def category_mean(int):
    category = c.get_category()
    k = 1
    while k-1 < len(category): 
        for i in category:
            if k == int:
                return i[0]
            k += 1

for transaction in res:
    amount = transaction[0]
    date = transaction[1]
    description = transaction[2]
    category = transaction[4]
    type_transaction = "Доход" if transaction[3] == 1 else "Расход"
    
    formatted_description = description
    
    delimiter(1)
    print(f"Сумма:      {amount}")
    print(f"Дата:       {date}")
    print(f"Описание:   {formatted_description}")
    print(f"Категория:  {category_mean(category)}")
    print(f"Тип:        {type_transaction}")
else:
    print("Ниичего не найдено")