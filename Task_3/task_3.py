# -*- coding: utf-8 -*-
import pandas as pd
import os

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # Выполняем left merge, чтобы сопоставить заказы с клиентами
    df = customers.merge(orders, left_on='id', right_on='customerId', how='left', suffixes=('_cust', '_ord'))

    # Фильтруем строки, где id заказа пустой
    result = df[df['id_ord'].isna()]

    # Выбираем только колонку name и переименовываем её
    result = result[['name']].rename(columns={'name': 'Customers'})

    return result

# Пример данных
customers_data = {'id': [1, 2, 3, 4], 'name': ['Joe', 'Henry', 'Sam', 'Max']}
orders_data = {'id': [1, 2], 'customerId': [3, 1]}

customers_df = pd.DataFrame(customers_data)
orders_df = pd.DataFrame(orders_data)

# Вызов функции
no_orders_df = find_customers(customers_df, orders_df)

# Сохранение результата
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'customers_without_orders.csv')
no_orders_df.to_csv(output_path, index=False)

print(f"Результат сохранен в {output_path}")
print("\nКлиенты, которые ничего не заказывали:")
print(no_orders_df.to_string(index=False))