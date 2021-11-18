"""
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
в соответствующий список. Должно получиться четыре списка — например,
os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import chardet
import re
import os

main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']


def get_file_list():
    """
    получаем все файлы в текущей папке с info в названии
    """
    return [list for list in os.listdir(path=".") if 'info' in list]


def get_data():
    """
    надеюсь тут правильно понял задумку авторов задачи с кучей листов для каждого параметра
    """
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file_info in get_file_list():
        with open(file_info, 'rb') as file:
            result = chardet.detect(file.read())
            # print(f'кодировка файла - {result["encoding"]}\n')

        with open(file_info, encoding=result["encoding"]) as file:
            text = file.read()
            os_prod_list.append(re.search(fr'{main_data[0]}:\s+(.*)', text).group(1))
            os_name_list.append(re.search(fr'{main_data[1]}:\s+(.*)', text).group(1))
            os_code_list.append(re.search(fr'{main_data[2]}:\s+(.*)', text).group(1))
            os_type_list.append(re.search(fr'{main_data[3]}:\s+(.*)', text).group(1))

    final_result = [main_data]

    for id, value in enumerate(get_file_list()):
        final_result.append([os_prod_list[id], os_name_list[id], os_code_list[id], os_type_list[id]])

    return final_result


def write_to_csv():
    with open('task_1_data_write.csv', 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in get_data():
            f_n_writer.writerow(row)


write_to_csv()

with open('task_1_data_write.csv', encoding='utf-8') as f_n:
    print(f_n.read())
