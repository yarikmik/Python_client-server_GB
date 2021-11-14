'''
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
'''


def check_byte_type(list):
    for word in list:
        try:
            b_word = eval(f"b'{word}'")
            print(f'"{word}" - возможна запись в байтовом типе: {b_word}')
        except:
            print(f'"{word}" - НЕвозможна запись в байтовом типе')


str_list = ['attribute', 'класс', 'функция']

check_byte_type(str_list)
