#coding=utf-8
#！/usr/bin/env python3


import os

import socket

server = socket.socket()
server.bind(('localhost',6969))
server.listen()
conn,addr =server.accept()
conn.close()