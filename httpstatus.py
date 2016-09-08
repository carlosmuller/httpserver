# -*- coding: UTF-8 -*-
class httpstatus(object):
    """Enum para facilitar o envio da resposta"""
    status = {200: '200 OK', 400: '400 Bad Request', 404: '404 Not Found', 415: '415 Unsupported Media Type',
              500: '500 Internal Server error', 501: '501 Not Implemented'}
