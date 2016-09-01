# -*- coding: UTF-8 -*-
import logging
import thread

from httpmethods import httpmethod
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
        headerRequest = msg.split('\r\n')[0]
        logger.info('Cliente [%s] pediu %s com a mensagem completa:\n%s' % (self.cliente, headerRequest, msg))
        method = headerRequest.split(' ')[0].upper()
        if method not in httpmethod.allmethods():
            self.sendResponse("This method [%s] is not implemented yet" % method, httpstatus.status[501])
        else:
            self.sendResponse(msg,httpstatus.status[200])
        thread.exit()

    def sendResponse(self, msg, status):
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(msg),
            'Connection': 'close',
        }
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
        response_proto = 'HTTP/1.0'
        self.conexao.send('%s %s' % (response_proto, status))
        self.conexao.send(response_headers_raw)
        result = '\n<html><body>' + msg.replace('\r\n', '<br>') + '</body></html>'
        self.conexao.send(result)
        self.conexao.close()
        # logger.info('Respondi o cliente [%s] com o status [%s] e a mensagem:\n%s' % (self.cliente, status, msg))
