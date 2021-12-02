"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import logs.config_client_log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
from errors import ReqFieldMissingError

# Инициализируем клиентский логгер
CLIENT_LOGGER = logging.getLogger('client')


def create_message(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def server_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def get_argv():
    '''Загружаем параметы коммандной строки
    client.py 127.0.0.1 8888
    '''
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
        CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}')
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.warning(f'Ошибка параметров запуска клиента, '
                              f'применены значения по умолчанию, адрес сервера: {server_address} , порт: {server_port}')
    except ValueError:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        # print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    return server_address, server_port


class ClientSocket(object):

    def __init__(self, ip='', port=''):
        self.server_port = port
        self.server_address = ip

    def __connect_to_server(self):
        try:
            self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.transport.connect((self.server_address, self.server_port))
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}, '
                                   f'конечный компьютер отверг запрос на подключение.')

    def print_client_params(self):
        print(f'Порт сервера:{self.server_port}, адрес:{self.server_address}')

    def client_init(self):
        self.__connect_to_server()
        message_to_server = create_message()
        send_message(self.transport, message_to_server)
        try:
            answer = server_ans(get_message(self.transport))
            CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        except (ValueError, json.JSONDecodeError):
            CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')

        except ReqFieldMissingError as missing_error:
            CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')

    def get_sent_message(self):
        """функция для юнит теста"""
        return create_message()

    def get_answer_message(self):
        """функция для юнит теста"""
        self.__connect_to_server()
        message_to_server = create_message()
        send_message(self.transport, message_to_server)
        return server_ans(get_message(self.transport))


if __name__ == '__main__':
    ip, port = get_argv()

    client = ClientSocket(ip, port)
    client.print_client_params()
    client.client_init()

    # print(client.get_sent_message())
    # print(client.get_answer_message())
