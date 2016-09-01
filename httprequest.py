# -*- coding: UTF-8 -*-
import logging
import thread
from httpstatus import *

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
PACKET_LENGTH = 32


class httprequest(object):
    """Classe de processamento do http e da requisição"""

    def __init__(self, conexao, cliente):
        self.conexao = conexao
        self.cliente = cliente[0]

    def processarRequest(self):
        msg = ""
        while True:
            tmp = self.conexao.recv(PACKET_LENGTH)
            msg += tmp
            if len(tmp) < PACKET_LENGTH:
                break
        self.sendResponse(msg)
        logger.info('Cliente [%s] pediu %s com a mensagem completa:\n%s' % (self.cliente, msg.split('\r\n')[0], msg))
        thread.exit()

    def sendResponse(self, msg):
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(msg),
            'Connection': 'close',
        }
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
        response_proto = 'HTTP/1.0'
        self.conexao.send('%s %s' % (response_proto, httpstatus.status[200]))
        self.conexao.send(response_headers_raw)
        result = '\n<html><body>' + msg.replace('\r\n', '<br>') + '</body></html>'
        self.conexao.send(result)
        self.conexao.close()