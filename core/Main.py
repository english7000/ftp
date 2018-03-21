#coding=utf-8
#！/usr/bin/env python3


from core import client
import getpass

def run():
    client_instance = client.user()
    client_instance.connect('localhost', 6967)

    count = 3
    while count > 0:
        name = input('name:')
        passwd = getpass.getpass('passwd:')
        if count == 0:
            exit()
        if client_instance.login(name, passwd):
            while True:
                command = input('>>:')
                client_instance.exec_command(command)
        else:
            count -= 1
            continue