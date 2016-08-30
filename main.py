import thread
import socket
import argparse
import logging
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


def conected(socket,client):
    # need to shpw to do this while until msg  ends for really long url
    msg = ""
    while True:
        tmp = socket.recv(PACKET_LENGTH)
        msg += tmp
        if (len(tmp) < PACKET_LENGTH):
            break
    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(msg),
        'Connection': 'close',
    }
    response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
    response_proto = 'HTTP/1.1'
    response_status = '200'
    response_status_text = 'OK'
    socket.send('%s %s %s' % (response_proto, response_status, response_status_text))
    socket.send(response_headers_raw)
    result = '\n<html><body>' + msg.replace('\r\n', '<br>') + '</body></html>'
    logger.info('Cliente [%s] pediu %s'%(client,msg.split('\r\n')[0]))
    #print msg.split('\r\n')[0].split(' ')[1]
    socket.send(result)
    socket.close()
    thread.exit()


if __name__ == '__main__':
    port = get_args()
    if port:
        PORT = port

    print 'Starting server at', PORT

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    orig = ('0.0.0.0', PORT)
    tcp.bind(orig)

    tcp.listen(1)
    try:
        while True:
            con, client = tcp.accept()
            thread.start_new_thread(conected, (con,client))
    except Exception as e:
        print e
        tcp.close()
