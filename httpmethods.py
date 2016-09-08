# -*- coding: UTF-8 -*-
class httpmethod(object):
    get = 'GET'
    post = 'POST'
    head = 'HEAD'

    @staticmethod
    def allmethods():
        return [httpmethod.get, httpmethod.post, httpmethod.head]
