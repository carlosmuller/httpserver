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
        header = linhas_request[0].split(' ')
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

    @property
    def path(self):
        return self.__header.path
