# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class BaseAdapter(object):
    def __init__(self, auth):
        self.auth = auth

    def send(self, number, message, **kwargs):
        raise NotImplementedError

    def call(self, number, code, **kwargs):
        pass

    def call_is_available(self):
        return False

    def call_digits(self):
        return 4


class ConsoleAdapter(BaseAdapter):
    def send(self, number, message, **kwargs):
        print('')
        print('Sent to {0} message "{1}"'.format(number, message))
        print('')


class AdapterError(Exception):
    pass
