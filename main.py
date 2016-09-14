# -*- coding: UTF-8 -*-
import thread
import socket
import argparse
import logging
from httphandler import *

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

help = """
HttpServer
    Usage:
        main.py Defaults to run on localhost:8181 with a packet size of 32 bytes
        main.py (-c | --config-file) <FILE>, must be an existing json file
    Option:
        -c , --config-file
"""

config = {
    'port':8181,
    'packet_length':32,
    'allow_serve_directories':False,
    'security':
    {
        'basic_auth':'root:toor',
        'private_directories':
        [
            'restrito'
        ]
    }
}

def parse_config_file(file):
    pass

def get_args():
    parser = argparse.ArgumentParser(
        description="A Simple HTTP server, if none where specified  will run on 8181 and packet size will be 32, with no password protection an will be")
    parser.add_argument('-c','--config-file', type=str, help='Config file, must be an existing json file. An example file is provided in config.json.sample')
    arg = parser.parse_args()
    parse_config_file(arg.config_file)

if __name__ == '__main__':

    logger.info('Starting server at %s' % config['port'])

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    # Aceita qualquer requeste de qualquer endereço, que venha na porta
    orig = ('0.0.0.0', config['port'])
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind(orig)
    # Começa a ouvir
    tcp.listen(100)
    try:
        while True:
            # Conexão aceita
            con, client = tcp.accept()
            logger.debug("Concetado com cliente %s" % client[0])
            # Criando obj para parsear o request
            request = httphandler(con, client, config['packet_length'])
            # Start em uma nova thread e procesa a request
            thread.start_new_thread(request.processarRequest, ())
    except KeyboardInterrupt as e:
        print "Servidor finalizado com sucesso"
    except Exception as e:
        print "Servidor encontrou um problema", e
    finally:
        tcp.listen(0)
        tcp.close()
