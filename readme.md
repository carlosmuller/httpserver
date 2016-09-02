### HttpServer based on version 1.0 defined in RFC-1945
  - See: http://www.faqs.org/rfcs/rfc1945.html

HttpServer
    Usage:
        main.py , will run on 8181 and packet size will be 32
        main.py (-p | --port) <PORT> , must be greater than 1024
        main.py (-l | --length) <LENGTH>, packet size must be greater than 0
    Option:
        -p, --port
        -l , --length