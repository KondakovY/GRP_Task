# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Настройки путей
input_file = 'measurements.csv'
output_dir = 'output'
figures_dir = 'output/figures'

os.makedirs(figures_dir, exist_ok=True)

# 1. Загрузка данных
df = pd.read_csv(input_file)

# 2. Часть 1 — Таблица метрик
def get_group_metrics(group):
    return pd.Series({
        'n': group['value'].count(),
        'mean': group['value'].mean(),
        'std': group['value'].std(),
        'corr': group['day'].corr(group['value'])
    })

metrics_df = df.groupby('series').apply(get_group_metrics, include_groups=False).reset_index()
metrics_df = metrics_df[['series', 'n', 'mean', 'std', 'corr']]
metrics_df = metrics_df.sort_values('series')

# Сохранение
metrics_df.to_csv(os.path.join(output_dir, 'metrics.csv'), index=False)
print("Файл metrics.csv сохранен.")

# 3. Часть 2 — Графики
sns.set_theme(style='whitegrid')

# График A — динамика (trends.png)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='day', y='value', hue='series', marker='o')
plt.title('Динамика показателей по дням')
plt.xlabel('День')
plt.ylabel('Значение')
plt.savefig(os.path.join(figures_dir, 'trends.png'), dpi=300)
plt.close()

# График B — сравнение средних (means_bar.png)
plt.figure(figsize=(8, 6))
sns.barplot(data=metrics_df, x='series', y='mean', hue='series', palette='viridis', legend=False)
plt.title('Сравнение средних значений')
plt.xlabel('Серия')
plt.ylabel('Среднее значение')
plt.savefig(os.path.join(figures_dir, 'means_bar.png'), dpi=300)
plt.close()

print("Графики сохранены в output/figures/")
print("\nИтоговые метрики:")
print(metrics_df.to_string(index=False))