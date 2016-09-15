# -*- coding: UTF-8 -*-
import logging
import thread

from httprequest import *
from httpstatus import *
from file import *

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class httphandler(object):
    """Classe de processamento do http e da requisição"""

    def __init__(self, conexao, cliente, packet_length, security):
        self.conexao = conexao  # socket
        self.cliente = cliente  # Cliente ip porta
        self.packet_length = packet_length  # tamanho para leitura de entrada
        self.security = security

    """
        Método que recebe toda a mensagem to cliente e a valida,
        para cada tipo de erro manda uma saída.
    """

    def processarRequest(self):
        msg = ""
        # Recebe a mensgem até ela acabar
        while True:
            tmp = self.conexao.recv(self.packet_length)
            msg += tmp
            if len(tmp) < self.packet_length:
                break
        logger.info('Cliente(ip, porta resposta ) [%s] com a mensagem completa:\n%s' % (self.cliente, msg))
        try:
            # Monta o que é necessário para responder, caso tenha algo invalido ele lança exceção
            request = HttpRequest(msg)
            self.request = request
            #See
            if any(request.path.startswith('/'+directory) for directory in self.security['private_directories']):
                if not request.authorization:
                    return self.send_401()
                else:
                    if self.security['basic_auth'] == request.authorization:
                        # Tenta ler o arquivo, caso não ache lança uma IOeror e cai no return 404
                        file = File(request.path)
                        # Chama o  métoodo de resposta
                        self.sendResponse(file.content, file.mime_type, httpstatus.status[200])
                        return
                    else:
                        return self.send_401()
            # Tenta ler o arquivo, caso não ache lança uma IOeror e cai no return 404
            file = File(request.path)
            # Chama o  métoodo de resposta
            self.sendResponse(file.content, file.mime_type, httpstatus.status[200])
        except (HeaderInvalidException, HeaderInvalidProtocolException) as ie:
            response_body = ie.message
            self.sendResponse(response_body, file_type['html']['mime_type'], httpstatus.status[400])
        except HeaderMethodException as header_method:
            response_body = header_method.message
            self.sendResponse(response_body, file_type['html']['mime_type'], httpstatus.status[501])
        except IOError as e:
            self.sendResponse(httpstatus.status[404], file_type['html']['mime_type'], httpstatus.status[404])
        except Exception as e:
            response_body = e.message
            self.sendResponse(response_body, file_type['html']['mime_type'], httpstatus.status[500])
        finally:
            # Depois de enviar a resposta ele fecha a thread em que ele está executando
            thread.exit()

    def send_401(self):
        self.sendResponse(httpstatus.status[401], file_type['html']['mime_type'], httpstatus.status[401])
        return

    """
        Método que responde o cliente com uma msg em html, e um status
    """

    def sendResponse(self, response_body, mime_type, status):
        response_proto = 'HTTP/1.0'
        # Caso retorne algum erro monta um  body com a mensagem do erro
        if status != httpstatus.status[200] and status != httpstatus.status[401]:
            response_body = '<html><body><h1>' + response_body + '</h1></body></html>'
        # Builder do cabeçalho a partir do conteudo da mensagem
        if status == httpstatus.status[401]:
            response_headers = self.buildHeaders(mime_type, response_body, True)
        else:
            response_headers = self.buildHeaders(mime_type, response_body)

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
        self.conexao.send('%s %s\r\n' % (response_proto, status))
        self.conexao.send(response_headers_raw)
        self.conexao.send('\r\n%s' % response_body)
        self.conexao.close()
        logger.info('Respondemos para o Cliente [%s] com o status [%s] com a header:\n%s\n' % (
            self.cliente, status, response_headers))

    def buildHeaders(self, mime_type, response, authentication=None):
        if authentication is None:
            response_headers = {
                'Content-Type': mime_type,
                'Content-Length': len(response),
                'Connection': 'close',
            }
            return response_headers
        response_headers = {
            'Content-Type': mime_type,
            'Content-Length': len(response),
            'Connection': 'close',
            'WWW-Authenticate': 'Basic realm="%s"' % self.security['realm']
        }
        return response_headers
