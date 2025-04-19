import requests
import time
import json  # Для форматирования JSON
from datetime import datetime

headers = {"X-Token": "uDn5bBm6IEE6T3FN9XM2uyr8Ce7BqJPvyDUDe_PmdgoU"}
url = "https://api.monobank.ua/personal/statement/{account}/{from_date}/{to_date}" # URL для получения транзакций

try:
    # Укажите параметры: account (номер счета), from_date (начало периода), to_date (конец периода)
    start_date = input("Введите дату начала периода (YYYY MM DD): ")  # Начало периода (YYYY-MM-DD)
    end_date = input("Введите дату конца периода (YYYY MM DD): ")  # Конец периода (YYYY-MM-DD)
    
    # Преобразуем строки в объекты datetime
    start_date_obj = datetime.strptime(start_date, "%Y %m %d")  # Преобразуем начало периода
    end_date_obj = datetime.strptime(end_date, "%Y %m %d")  # Преобразуем конец периода

    # Преобразуем объекты datetime в timestamp
    from_timestamp = int(start_date_obj.timestamp())  # Начало периода
    to_timestamp = int(end_date_obj.timestamp())  # Конец периода
except ValueError:
    print("Ошибка: неверный формат даты. Пожалуйста, используйте формат YYYY MM DD.")
    input("\nНажмите Enter, чтобы выйти...")
account = "0"  # Замените на ID счета    
# Формируем URL с параметрами
url = url.format(account=account, from_date=from_timestamp, to_date=to_timestamp)
# Вполняем запрос
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверяем статус ответа
    print(f"Статус ответа: {response.status_code}")
    # Обрабатываем JSON-ответ
    transactions = response.json()
    if transactions:
        print(f"Список транзакций за {time.strftime('%Y.%m.%d',time.localtime(from_timestamp))+' - '+time.strftime('%Y.%m.%d',time.localtime(to_timestamp))}:") #список транзакций за указанный период
        for idx, transaction in enumerate(transactions, start=1):
            transaction_time = transaction.get("time", "Не указано")
            description = transaction.get("description", "Нет описания")
            amount = transaction.get("amount", "Не указано")
            balance = transaction.get("balance", "Не указано")
            if isinstance(amount,(int, float)):
                amount = f"{amount / 100:.2f}" + " грн"
            if isinstance(balance,(int, float)):
                balance = f"{balance / 100:.2f}" + " грн"
            transaction_date = time.strftime("%Y.%m."
            "%d", time.localtime(transaction_time))
            transaction_time = time.strftime("%H:%M:%S", time.localtime(transaction_time))
            
            print(f"\nТранзакция #{idx}:")  
            print(f"Дата: {transaction_date}\nВремя: {transaction_time}\nОписание: {description}\nСумма: {amount}\nБаланс: {balance}")
            # print(json.dumps(transaction, indent=4, ensure_ascii=False)) 
    else:
        print("Нет транзакций за указанный период.")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
# Подсчитываем сумму потраченных средств (только отрицательные значения)
spent_amount = sum(t["amount"] for t in transactions if t["amount"] < 0) / 100
print(f"\nОбщая сумма потраченных средств за указанный период: {spent_amount:.2f} грн")

input("\nНажмите Enter, чтобы выйти...")