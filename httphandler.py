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
    mime_jpg = "image/jpg"
    mime_gif = "image/gif"
    mime_css = "text/css; encoding=utf8"
    mime_ico = "image / x - icon"

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
            arquivo_path = "."+request.path
            if arquivo_path == './':
                arquivo_path = 'index.html'
            if arquivo_path.endswith('htm') or arquivo_path.endswith('html'):
                arquivo = open(arquivo_path, 'r')
                response_body = arquivo.read()
                self.sendResponse(response_body, self.mime_html, httpstatus.status[200])
                arquivo.close()
            elif arquivo_path.endswith(('jpeg', 'jpg')):
                # rb porque é binary
                arquivo = open(arquivo_path, 'rb')
                response_body = arquivo.read()
                arquivo.close()
                self.sendResponse(response_body, self.mime_jpg, httpstatus.status[200])
            elif arquivo_path.endswith('css'):
                arquivo = open(arquivo_path, 'r')
                response_body = arquivo.read()
                arquivo.close()
                self.sendResponse(response_body, self.mime_css, httpstatus.status[200])
            elif arquivo_path.endswith('gif'):
                arquivo = open(arquivo_path, 'rb')
                response_body = arquivo.read()
                arquivo.close()
                self.sendResponse(response_body, self.mime_gif, httpstatus.status[200])
            elif arquivo_path.endswith('ico'):
                arquivo = open(arquivo_path, 'rb')
                response_body = arquivo.read()
                arquivo.close()
                self.sendResponse(response_body, self.mime_ico, httpstatus.status[200])

            else:
                self.return404()
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
        response_proto = 'HTTP/1.0'
        if status != httpstatus.status[200]:
            response_body = '\r\n<html><body>' + response_body + '</body></html>'
        response_headers = self.mountResponseHeader(mime_type, response_body)
        logger.info("Respondemos para o Cliente [%s] com o status [%s] com a header:\n%s" % (
            self.cliente, status, response_headers))
        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
        self.conexao.send('%s %s\r\n' % (response_proto, status))
        self.conexao.send(response_headers_raw)
        self.conexao.send("\r\n" + response_body)
        self.conexao.close()
        # logger.info('Respondi o cliente [%s] com o status [%s] e a mensagem:\n%s' % (
        # self.cliente, status, (response_headers + response_body)))

    def mountResponseHeader(self, mime_type, response):
        response_headers = {
            'Content-Type': mime_type,
            'Content-Length': len(response),
            'Connection': 'close',
        }
        return response_headers
