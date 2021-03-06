# -*- coding: UTF-8 -*-
from httpmethods import httpmethod


class HeaderInvalidException(Exception):
    """ Execeção levantada quando o header não possui  metodo,path,porotocolo"""

    def __init__(self, message):
        self.message = message


class HeaderMethodException(Exception):
    """ Execeção levantada quando o method não é válido """

    def __init__(self, message):
        self.message = message


class HeaderInvalidProtocolException(Exception):
    """ Execeção levantada quando o protocolo não é valido"""

    def __init__(self, message):
        self.message = message


class HttpHeader(object):
    """Classe que representa o header de um http request"""
    method = ''
    path = ''
    protocol = ''


class HttpRequest(object):
    """Classe que monta um http request e o valida"""

    def __init__(self, msg):
        self.__header = HttpHeader()
        self.__msg = msg
        # Pega o header da requisão
        linhas_request = msg.split('\r\n')
        # Separa o header en método, path e protocolo
        self.__first_line = linhas_request[0]
        header = self.__first_line.split(' ')
        # Válida que o header representa um header http 1.X
        if len(header) != 3:
            raise HeaderInvalidException('Esse cabeçalho é invalido[%s] para requisições HTTP/1.0' % header)
        self.__header.method = header[0]
        path_with_params = header[1].split('?')
        self.__header.path = path_with_params[0]
        if len(path_with_params) > 1:
            self.__params = path_with_params[1]
        self.__header.protocol = header[2]
        # Validação para o protocolo 1.0 ou 1.1
        if not self.__header.protocol.upper().startswith('HTTP/1'):
            raise HeaderInvalidProtocolException('Request inválido protocolo não aceito [%s]' % self.__header.protocol)
        # Apenas aceitamos HEAD, POST e GET
        if self.__header.method not in httpmethod.allmethods():
            raise HeaderMethodException('Esse método[%s] ainda ainda não foi implementado' % self.__header.method)
        if self.__header.method == httpmethod.post:
            content_length = filter(lambda x: x.startswith('Content-Length'), linhas_request)
            if not content_length or content_length[0].split(':')<0:
                raise HeaderInvalidException('Para requisições com metódo [POST] precisamos de um tamanho')

        self.__authorization = filter(lambda x: x.startswith('Authorization:'), linhas_request)

    @property
    def path(self):
        return self.__header.path

    @property
    def header(self):
        return self.__first_line

    @property
    def method(self):
        return self.__header.method

    @property
    def authorization(self):
        if self.__authorization:
            return self.__authorization[0].split('Authorization: Basic ')[1]
        return None
