'''2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
'''


def converter(list):
    for word in list:
        b_word = eval(f"b'{word}'")
        print(f'{word}:\n{b_word} тип: {type(b_word)}, длина: {len(b_word)}')


str_list = ['class', 'function', 'method']

converter(str_list)
