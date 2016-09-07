# -*- coding: UTF-8 -*-
import logging
import thread

from httprequest import *
from httpstatus import *

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class httphandler(object):
    """Classe de processamento do http e da requisição"""
    mime_html = "text/html; encoding=utf8"

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
        logger.info('Cliente(ip, porta resposta ) [%s] com a mensagem completa:\n%s' % (self.cliente, msg))
        try:
            request = HttpRequest(msg)
            arquivo_path = None
            if request.path == '/':
                arquivo_path = 'index.html'
            elif request.path.endswith('htm') or request.path.endswith('html'):
                arquivo_path = request.path
            else:
                self.return404()
            if arquivo_path is None:
                self.return404()
            else:
                arquivo = open(arquivo_path, 'r')
                logger.info("Tentando abri arquivo %s" % arquivo.name)
                response_body = arquivo.read()
                self.sendResponse(response_body, self.mime_html, httpstatus.status[200])
                arquivo.close()
        except HeaderInvalidException as header_invalid:
            response_body = header_invalid.message
            self.sendResponse(response_body, self.mime_html, httpstatus.status[400])
        except HeaderInvalidProtocolException as invalid_protocol:
            response_body = invalid_protocol.message
            self.sendResponse(response_body, self.mime_html, httpstatus.status[400])
        except HeaderMethodException as header_method:
            response_body = header_method.message
            self.sendResponse(response_body, self.mime_html, httpstatus.status[501])
        except IOError as e:
            self.return404()
        except Exception as e:
            response_body = e.message
            self.sendResponse(response_body, self.mime_html, httpstatus.status[500])
        finally:
            # Depois de enviar a resposta ele fecha a thread em que ele está executando
            thread.exit()

    def return404(self):
        response_body = "Ops acho que perdemos alguma coisa :S"
        self.sendResponse(response_body, self.mime_html, httpstatus.status[404])

    """
        Método que responde o cliente com uma msg em html, e um status
    """

    def sendResponse(self, response_body, mime_type, status):
        logger.info("Respondemos para o Cliente [%s] com o status [%s] com a mensagem:\n%s" % (
            self.cliente, status, response_body))
        response_proto = 'HTTP/1.0'
        if status != httpstatus.status[200]:
            response_body = '\r\n<html><body>' + response_body + '</body></html>'
        response_headers = self.mountResponseHeader(mime_type, response_body)
        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())

        self.conexao.send('%s %s\r\n' % (response_proto, status))
        self.conexao.send(response_headers_raw)
        self.conexao.send("\r\n"+response_body)
        self.conexao.close()
        # logger.info('Respondi o cliente [%s] com o status [%s] e a mensagem:\n%s' % (self.cliente, status, msg))

    def mountResponseHeader(self, mime_type, response):
        response_headers = {
            'Content-Type': mime_type,
            'Content-Length': len(response),
            'Connection': 'close',
        }
        return response_headers
