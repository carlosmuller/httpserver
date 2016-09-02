# -*- coding: UTF-8 -*-
import thread
import socket
import argparse
import logging
from httprequest import *

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

help = """
HttpServer
    Usage:
        main.py , will run on 8181 and packet size will be 32
        main.py (-p | --port) <PORT> , must be greater than 1024
        main.py (-l | --length) <LENGTH>, packet size must be greater than 0
    Option:
        -p, --port
        -l , --length
"""


def get_args():
    parser = argparse.ArgumentParser(description="A Simple HTTP server, if none where specified  will run on 8181 and packet size will be 32")
    parser.add_argument('-p', '--port', type=int, help='Port number, must be greater than 1024',
                        required=False, nargs='?', default=8181)
    parser.add_argument('-l', '--length', type=int, help='Packet size, must be greater than 0',
                        required=False, nargs='?', default=32)
    args = parser.parse_args()
    return args.port, args.length


if __name__ == '__main__':
    PORT, PACKET_LENGTH = get_args()

    logger.info('Starting server at %s' % PORT)

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    #Aceita qualquer requeste de qualquer endereço, que venha na porta
    orig = ('0.0.0.0', PORT)
    tcp.bind(orig)
    #Começa a ouvir
    tcp.listen(1)
    try:
        while True:
            #Conexão aceita
            con, client = tcp.accept()
            logger.debug("Concetado com cliente %s" % client[0])
            #Criando obj para parsear o request
            request = httprequest(con, client, PACKET_LENGTH)
            #Start em uma nova thread e procesa a request
            thread.start_new_thread(request.processarRequest, ())
    except Exception as e:
        tcp.listen(0)
        tcp.close()
        print e
