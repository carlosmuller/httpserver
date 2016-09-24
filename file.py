# -*- coding: UTF-8 -*-
import re as regex
from os import listdir
from os import path as ospath
from mimetypes import MimeTypes

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
    def __init__(self, path, serve_directory):
        # Append para servir do diretório para baixo
        path = regex.sub(r"/+", "/", path)
        path = '.' +path
        self.__is_directory = ospath.isdir(path)
        self.__serve_directory = serve_directory
        # Caso a opção não servimos direórios servimos um index.html
        if self.__is_directory:
            if not serve_directory:
                path += 'index.html'

        self.__path = path
        # Caso aceite o tipo de arquivo mime type correto e o tipo de leitura, se não cai no padrão octet-stream
        try:
            self.__file_type = file_type[self.__extract_extension()]
        except KeyError:
            self.__file_type = file_type['default']

    @property
    def content(self):
        if self.__is_directory and self.__serve_directory:
            return self.mount_directory_list()
        else:
            file = open(self.__path, self.__file_type['read_type'])
            content = file.read()
            file.close()
            return content

    @property
    def mime_type(self):
        if self.__file_type == file_type['default']:
            mime = MimeTypes()
            guessed = mime.guess_type(self.__path)
            if guessed[0] is not None:
                return guessed[0]
        return self.__file_type['mime_type']

    def __extract_extension(self):
        split = self.__path.split('.')
        return split[len(split) - 1]

    #Montamos um html com uma lista de arquivos e diretórios do path
    def mount_directory_list(self):
        list = listdir(self.__path)
        self.__file_type = file_type['html']
        hidden_item = '<li hidden></li>'
        path = self.__path[self.__path.find('/')+1:]
        list_item = '<li><a href="%s">%s</li>' + hidden_item
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Arquivos em: [%s]</title></head><body><h1>Lista de arquivos:</h1><ul>%s</ul></body></html>' % (
        self.__path, hidden_item)
        for item in list:
            content = content.replace(hidden_item, list_item % (path+'/'+item, item))
        return content
