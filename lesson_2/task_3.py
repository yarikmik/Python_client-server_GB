"""
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с
помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import json
import yaml

with open('orders.json', encoding='utf-8') as f_n:
    f_n_content = f_n.read()
    objs = json.loads(f_n_content)

# данные для задания:
task_data = {'свойства': ['свойство_1', 'свойство_2'],
             'ответ а все': 42,
             'валюты': {'$': 'доллар', '₽': 'рубль', '€': 'евро'}}

# + данные json из второго задания:
yaml_data = [task_data, objs]

with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(yaml_data, f_n, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open('file.yaml', encoding='utf-8') as f_n:
    f_n_content = yaml.load(f_n, Loader=yaml.FullLoader)

print(f_n_content)


