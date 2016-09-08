# -*- coding: UTF-8 -*-
import re as regex

"""
    Mapa constante de definição para tipos de arquivos
"""
file_type = {
    'jpg': {
        'read_type': 'rb',
        'mime_type': 'image/jpg'
    },
    'jpeg': {
        'read_type': 'rb',
        'mime_type': 'image/jpeg'
    },
    'gif': {
        'read_type': 'rb',
        'mime_type': 'image/gif'
    },
    'html': {
        'read_type': 'r',
        'mime_type': 'text/html; encoding=utf8'
    },
    'htm': {
        'read_type': 'r',
        'mime_type': 'text/htm; encoding=utf8'
    },
    'ico': {
        'read_type': 'rb',
        'mime_type': 'image/x-icon'
    },
    'css': {
        'read_type': 'r',
        'mime_type': 'text/css; encoding=utf8'
    },
    'js': {
        'read_type': 'r',
        'mime_type': 'text/js; encoding=utf8'
    },
    'default': {
        'read_type': 'rb',
        'mime_type': 'application/octet­stream'
    }

}


class File(object):
    def __init__(self, path):
        # Append para servir do diretório para baixo
        path = regex.sub(r"/+", "/", path)
        if path.endswith('/'):
            path += 'index.html'
        self.__path = '.' + path
        # Caso aceite o tipo de arquivo mime type correto e o tipo de leitura, se não cai no padrão octet-stream
        try:
            self.__file_type = file_type[self.__extract_extension()]
        except KeyError:
            self.__file_type = file_type['default']

    @property
    def content(self):
        file = open(self.__path, self.__file_type['read_type'])
        content = file.read()
        file.close()
        return content

    @property
    def mime_type(self):
        return self.__file_type['mime_type']

    def __extract_extension(self):
        split = self.__path.split('.')
        return split[len(split) - 1]
