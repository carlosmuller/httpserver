# -*- coding: UTF-8 -*-
import thread
import socket
import argparse
import json
import logging
from httphandler import *
from base64 import b64encode as encode

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
    'port': 8181,
    'packet_length': 32,
    'allow_serve_directories': False,
    'security':
        {
            'realm': 'realm',
            'basic_auth': 'root:toor',
            'private_directories':
                [
                    'restrito'
                ]
        }
}


def parse_config_file(file):
    if file is None:
        return None
    try:
        fl = open(file)
        js = json.loads(fl.read())
        fl.close()
        return js

    except IOError as e:
        print "Can't open file", file
        print e
        return None


def get_args():
    parser = argparse.ArgumentParser(
        description="A Simple HTTP server, if none where specified  will run on 8181 and packet size will be 32, the directory 'restrito' has access with 'root:toor'")
    parser.add_argument('-c', '--config-file', required=False, type=str,
                        help='Config file, must be an existing json file. An example file is provided in config.json.sample')
    arg = parser.parse_args()
    return parse_config_file(arg.config_file)


if __name__ == '__main__':
    config_args = get_args()
    if config_args is not None:
        config = config_args
    config['security']['basic_auth']= encode(config['security']['basic_auth'])
    logger.info('Starting server at %s' % config['port'])

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    # Aceita qualquer requeste de qualquer endereço, que venha na porta
    orig = ('0.0.0.0', int(config['port']))
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
            request = httphandler(con, client, int(config['packet_length']), config['security'], config['allow_serve_directories'])
            # Start em uma nova thread e procesa a request
            thread.start_new_thread(request.processarRequest, ())
    except KeyboardInterrupt as e:
        print "Servidor finalizado com sucesso"
    except Exception as e:
        print "Servidor encontrou um problema", e
    finally:
        tcp.listen(0)
        tcp.close()
