# -*- coding: utf-8 -*-

from grab import Grab

try:
    from logger import Logger
except ImportError:
    pass

from config import Conf

__author__ = 'whoami'
__version__ = '1.3.3'
__date__ = '19.02.16 23:14'
__description__ = """
Набот методов для работы с апи
"""


class ApiMethods:
    BODY = 0
    JSON = 1

    online_only = None
    acc_status = None

    def __init__(self, loggining=False):
        if loggining:
            try:
                self.logger = Logger()
            except NameError:
                raise SystemExit('В данный момент логгер не поддерживается!')

        config = Conf(section='api')
        self.base_url = config.main_url

    def request(self, url='', origin=1, **kwargs):
        g = Grab()
        try:
            g.go(self.base_url + url, post=kwargs)
            response = g.response.json if origin else g.response.body
        except Exception as e:
            response = dict(error=e)
        finally:
            del g

        return response
