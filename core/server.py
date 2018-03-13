#coding=utf-8
#！/usr/bin/env python3


import socketserver
import os

class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request

        print(self.client_address)
        path = conn.recv(1024).decode()
        os.chdir(path)
        conn.send(os.popen('du -sk').read().encode('utf-8'))
        while True:
            command = conn.recv(1024).decode()
            # print(command)
            # print(command.strip().startswith('cd'))
            if command.strip() in ['ls', 'mkdir','pwd']:
                # print(command,1)
                data = os.popen(command).read()
                conn.send(str(len(data)).encode('utf-8'))                # 发送command结果的长度
                if conn.recv(1024).decode() == 'ready':
                    conn.send(data.encode('utf-8'))

            elif command.strip().startswith('cd'):
                print(111)
                os.chdir(command.strip().replace('cd ',''))
                conn.send(b'0')

            elif command.strip().startswith('put'):                 #上传
                file_name = command.replace('put ', '').split('/').pop()
                print(file_name)
                conn.send(b'ok')
                length = conn.recv(1024).decode()
                print(length)
                conn.send(b'ready')
                body = ''
                while len(body) < int(length):
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    body += data
                    print(body,1)
                with open(file_name, 'w') as f:
                    print(body)
                    f.write(body)

            elif command.strip().startswith('get'):                 #下载
                file_name = command.replace('get ', '').split('/').pop()
                print(file_name)
                with open(file_name,'r') as f:
                    body = ''
                    for line in f :
                        body += line
                length = len(body)
                print(length)
                conn.send(str(length).encode('utf-8'))
                if conn.recv(1024).decode() == 'ready':
                    conn.sendall(body.encode('utf-8'))







if __name__ == '__main__':

    server = socketserver.ThreadingTCPServer(('localhost', 6965), Myserver)  # 直接多线程实例化
    server.serve_forever()



