#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from requests import exceptions as RequestExceptions

from api_methods import ApiMethods
from config import Conf
from logger import Logger

__author__ = "wiom"
__version__ = "0.1.0"
__date__ = "27.07.16 3:57"
__description__ = """"""


def registration_user(user_info, phone_nomber):
    logger.info('Попытка регистрации номера {}. Отправитель: {}'.format(phone_nomber, user_info))
    if phone_nomber is None:
        return show_help(user_info, phone_nomber)
    user_info['tel'] = phone_nomber
    return 'Регистрация номера {} не удалась. Данная функциональность еще не реализована.'.format(phone_nomber)


def show_help(*args, **kwargs):
    logger.info('Вызов help message. {}'.format(*args, **kwargs))
    str_out = ''
    for key in command_help_list:
        value = command_help_list[key]
        str_out += '{}: {}\n'.format(key, value)

    return str_out


def check_phone(user_info, phone_nomber):
    logger.info('Попытка проверки номера {}. Отправитель: {}'.format(phone_nomber, user_info))
    user_info['tel'] = phone_nomber
    post_data = {'data': user_info}
    response = api.request(**post_data)
    if response.get('error'):
        response = 'Проверка номера {} неудалась. Попробуте повторить попытку позже'.format(phone_nomber)
    else:
        response = response['mess']
    return response


logger = Logger()
command_prefix = '/'
command_help_list = {'/reg': 'Регистрация. Если вы пользуетесь сервисом впервые, то отправьте сообщение "/reg +79990009900"',
                     '/help': 'Отображение этого сообщения',
                     '\nКак проверить номер': 'Для проверки номера телефона необходимо отправить мне сообщение с номером телефона в международном формате +79990009900\n'}
command_list = {'reg': registration_user,
                'help': show_help}

api = ApiMethods()
config = Conf(section='base')
djarvis = telebot.TeleBot(token=config.token, threaded=True)


@djarvis.message_handler(content_types=["text"])
def repeat_all_messages(request):
    logger.info('Получено сообщение с текстом: {}. Отправитель: {}'.format(request.text, request.from_user))
    body = request.text
    user_info = request.from_user.__dict__.copy()

    if body.startswith(command_prefix):
        command = body[1:].split(' ')
        if not command[0]:
            response = 'Хватит уже издеваться! После слеша нужно указать команду!\n{}'.format(show_help(user_info))
        else:
            if command[0] in command_list:
                response = command_list[command[0]](user_info, command[1] if len(command) > 1 else None)
            else:
                response = 'Неизвестная команда'
    else:
        response = check_phone(user_info, body)
    djarvis.send_message(request.chat.id, response)


if __name__ == '__main__':
    while True:
        print('Working on')
        try:
            djarvis.polling(none_stop=True)
        except KeyboardInterrupt:
            raise SystemExit('Working end. Goodbye!')
        except Exception as e:
            logger.warning(e)
            continue
