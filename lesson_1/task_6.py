'''
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

import locale
import chardet

with open('test_file.txt', 'rb') as file:
    result = chardet.detect(file.read())
    print(f'кодировка файла - {result["encoding"]}\n')

with open('test_file.txt', encoding='utf-8') as file:
    for line in file:
        print(line, end='')
    print()

default_encoding = locale.getpreferredencoding()
print(f'\nкодировка системы - {default_encoding}')
