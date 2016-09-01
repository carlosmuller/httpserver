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
        main.py , will run on 8080
        main.py (-p | --port) <PORT> , must be grereate than 1024

    Option:
        -p, --port
"""

PACKET_LENGTH = 32


def get_args():
    parser = argparse.ArgumentParser(description="A Simple HTTP server ")
    parser.add_argument('-p', '--port', type=int, help='Port number, must be greater than 1024',
                        required=False, nargs='?', default=8181)
    args = parser.parse_args()
    return args.port


if __name__ == '__main__':
    port = get_args()
    if port:
        PORT = port

    logger.info('Starting server at %s' % PORT)

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    orig = ('0.0.0.0', PORT)
    tcp.bind(orig)

    tcp.listen(1)
    try:
        while True:
            con, client = tcp.accept()
            logger.debug("Concetado com cliente %s" % client[0])
            request = httprequest(con, client)
            thread.start_new_thread(request.processarRequest, ())
    except Exception as e:
        tcp.close()
        print e
