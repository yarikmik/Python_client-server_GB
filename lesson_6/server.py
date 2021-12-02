"""Программа-сервер"""

import socket
import sys
import json
import logging
import logs.config_server_log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError
from decorators import log, LogClass

# Инициализируем серверный логгер
SERVER_LOGGER = logging.getLogger('server')


# @log
@LogClass()
def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param message:
    :return:
    '''
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


# @log
@LogClass()
def get_argv():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError

    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP_ADDRESS

    except IndexError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего параметра \'a\' '
                               f'необходимо указать адрес, который будет слушать сервер.')
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    return listen_address, listen_port


class ServerSocket(object):

    # @log
    @LogClass()
    def __init__(self, ip='', port=''):
        self.listen_port = port
        self.listen_address = ip
        SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {self.listen_port}, '
                           f'адрес с которого принимаются подключения: {self.listen_address}.')

    def print_server_params(self):
        print(f'Слушаем порт:{self.listen_port}, адрес:{self.listen_address}')

    # @log
    @LogClass()
    def server_init(self):
        # Готовим сокет
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.bind((self.listen_address, self.listen_port))
        # self.transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        # Слушаем порт
        self.transport.listen(MAX_CONNECTIONS)
        while True:
            client, client_address = self.transport.accept()
            SERVER_LOGGER.info(f'Установлено соедение с {client_address}')
            try:
                message_from_client = get_message(client)
                SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
                # print(message_from_cient)
                response = process_client_message(message_from_client)
                SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
                send_message(client, response)
                SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
                client.close()

            except (ValueError, json.JSONDecodeError):
                SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от '
                                    f'клиента {client_address}. Соединение закрывается.')
                client.close()
            except IncorrectDataRecivedError:
                SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                    f'Соединение закрывается.')
                client.close()


if __name__ == '__main__':
    ip, port = get_argv()

    server = ServerSocket(ip, port)
    server.print_server_params()
    server.server_init()

# server = ServerSocket()
# server.server_init()
