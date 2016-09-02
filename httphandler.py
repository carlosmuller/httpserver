# -*- coding: UTF-8 -*-
import logging
import thread

from httpmethods import httpmethod
from httpstatus import *

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class httphandler(object):
    """Classe de processamento do http e da requisição"""

    def __init__(self, conexao, cliente, PACKET_LENGTH):
        self.conexao = conexao  # socket
        self.cliente = cliente  # Cliente ip porta
        self.PACKET_LENGTH = PACKET_LENGTH  # tamanho para leitura de entrada

    """
        Método que recebe toda a mensagem to cliente e a valida,
        para cada tipo de erro manda uma saída.
    """

    def processarRequest(self):
        msg = ""
        # Recebe a mensgem até ela acabar
        while True:
            tmp = self.conexao.recv(self.PACKET_LENGTH)
            msg += tmp
            if len(tmp) < self.PACKET_LENGTH:
                break
        # Pega o header da requisão
        header = msg.split('\r\n')[0]
        # Separa o header en método, path e protocolo
        header_attributes = header.split(' ')
        logger.info('Cliente(ip, porta resposta ) [%s] pediu com o header [%s] com a mensagem completa:\n%s' % (self.cliente, header, msg))
        # Válida que o header representa um header http 1.X
        if len(header_attributes) != 3:
            self.sendResponse("Esse cabeçalho é invalido[%s] para requisições HTTP/1.0" % header, httpstatus.status[400])
        else:
            method = header_attributes[0].upper()
            path = header_attributes[1]
            protocol = header_attributes[2]
            # Validação para o protocolo 1.0 ou 1.1
            if not protocol.startswith("HTTP/1"):
                self.sendResponse("Request inválido protocolo não aceito [%s]" % protocol, httpstatus.status[400])
            else:
                # Apenas aceitamos HEAD, POST e GET
                if method not in httpmethod.allmethods():
                    self.sendResponse("Esse método[%s] ainda ainda não foi implementado" % method, httpstatus.status[501])
                else:
                    self.sendResponse(msg, httpstatus.status[200])
        # Depois de enviar a resposta ele fecha a thread em que ele está executando
        thread.exit()

    """
        Método que responde o cliente com uma msg em html, e um status
    """

    def sendResponse(self, msg, status):
        logger.info("Respondemos para o Cliente [%s] com o status [%s] com a mensagem:\n%s" % (self.cliente, status, msg))
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(msg),
            'Connection': 'close',
        }
        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
        response_proto = 'HTTP/1.0'
        self.conexao.send('%s %s\r\n' % (response_proto, status))
        self.conexao.send(response_headers_raw)
        result = '\n<html><body>' + msg.replace('\r\n', '<br>') + '</body></html>'
        self.conexao.send(result)
        self.conexao.close()
        # logger.info('Respondi o cliente [%s] com o status [%s] e a mensagem:\n%s' % (self.cliente, status, msg))
