'''
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
из байтовового в строковый тип на кириллице.
'''

import subprocess

import chardet


def ping_function(address):
    args = ['ping', address, '-n', '5']
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in subproc_ping.stdout:
        # print(line.decode('cp866').strip())
        result = chardet.detect(line)
        # print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8').strip())


ping_function('yandex.ru')
ping_function('youtube.com')
