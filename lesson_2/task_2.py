"""
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных
в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(item='', quantity='', price='', buyer='', date=''):
    with open('orders.json', encoding='utf-8') as f_n:
        f_n_content = f_n.read()
        objs = json.loads(f_n_content)

    order_dict = {'Товар': item,
                  'Колличество': quantity,
                  'Цена': price,
                  'Покупатель': buyer,
                  'Дата': date}

    objs['orders'].append(order_dict)
    with open('orders.json', 'w', encoding='utf-8') as f_n:
        json.dump(objs, f_n, ensure_ascii=False, indent=4)


write_order_to_json(item='Компьютер', quantity=13, price=40000)
write_order_to_json(item='Флешка', quantity=150, price=1500, buyer='человек', date='сегодня')
write_order_to_json(item='Монитор', price=25000, quantity=2)

with open('orders.json', encoding='utf-8') as f_n:
    print(f_n.read())

