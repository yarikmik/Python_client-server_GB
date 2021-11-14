'''
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
'''


def converter(list):
    for word in list:
        b_word = word.encode('utf-8')
        print(f'"{word}" -> {b_word}')
        str_word = b_word.decode('utf-8')
        print(f'"{b_word}" -> {str_word}\n')


str_list = ['разработка', 'администрирование', 'protocol', 'standard']

print()
converter(str_list)
