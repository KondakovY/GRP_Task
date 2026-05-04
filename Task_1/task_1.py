# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime
# import glob

input_path = 'data/tech_screen_sample.csv'
output_path = 'output/result.csv'

# Подготовка структуры папок
os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

# --- Дополнительная логика выбора файлов ---
# # Выбор самого последнего загруженного файла:
# files = glob.glob('data/*.csv')
# if files:
#     input_path = max(files, key=os.path.getctime)
#
# # Использование меток времени для выходных файлов:
# now = datetime.now().strftime('%Y%m%d_%H%M%S')
# output_path = f'output/result_{now}.csv'
# -------------------------------------------

# Обработка данных
df = pd.read_csv(input_path)
df = df[df['value'] >= 0]
df = df.drop_duplicates(subset=['batch', 'record_id'], keep='first')

# Расчет метрик по партиям
result = df.groupby('batch').agg(
    count=('value', 'count'),
    total=('value', 'sum')
).reset_index().sort_values('batch')

result['total'] = result['total'].round(2)

# Экспорт результата
result.to_csv(output_path, index=False)

# --- Очистка после обработки ---
# if os.path.exists(input_path):
#     os.remove(input_path)
# -------------------------------

print(f"Обработан файл: {input_path}")
print(f"Результат сохранен в: {output_path}")
print(result)