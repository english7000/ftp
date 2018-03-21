#coding=utf-8
#！/usr/bin/env python3


import os
import  socket
import getpass
from core.processbar import processbar

class user(object):
    '''用户类'''


    def __init__(self):
        # self.name = name
        # self.passwd = passwd
        # self.homedir = homedir
        # self.quote = quote            #配额
        self.conn = ''

    def login(self,name,passwd):
        self.conn.send(bytes(name,encoding='utf-8'))

        name_check = self.conn.recv(1024)
        if name_check == b'ok':
            self.conn.send(bytes(passwd,encoding='utf-8'))
            passwd_check = self.conn.recv(1024)
            if passwd_check ==b'ok':
                print('welcome back! %s' %name)
                print(self.conn.recv(1024).decode())
                return 1                            #认证成功
            else:
                print('Wrong passwd!')
                return 0

        else:
            print('no username :' ,name)
            return 0                                #认证失败


    def connect(self, ip,port):
        client =socket.socket()
        client.connect((ip,port))
        self.conn = client

    def exec_command(self,command):
        if command.strip().split(' ')[0] in ['ls','cd','mkdir','pwd']:
            self.conn.send(command.encode('utf-8'))             #ls和cd命令发送给server执行并收取结果
            length = self.conn.recv(1024).decode()                #接受命令结果长度
            self.conn.send(b'ready')
            print(length)
            if length:
                body = ''
                while len(body) < int(length):                           #循环接受结果
                    data = self.conn.recv(1024).decode()
                    body += data
                print(body)
            else:                                               #当长度为0的时候pass
                print('no output')

        elif 'put' in command.strip():                          #put和get代表上传和下载，传给自己的put和get方法
            self.put(command)                                   #path传入put方法
        elif 'get' in command.strip():
            self.get(command)                                   #path传入put方法

    def put(self,command):                                       #上传文件
        self.conn.send(command.encode('utf-8'))
        flag = self.conn.recv(1024)                                        #ok
        if flag == b'ok':
            file_name = command.strip().replace('put ','').split('/').pop()
            # length =os.popen("ls -l %s |awk '{print $5}' " %file_name).read()
            length = os.stat('%s' % file_name).st_size
            self.conn.send(bytes(str(length),encoding='utf-8'))
            _seek = self.conn.recv(1024).decode()                       #接受断点续传
            if _seek == 'no space left':
                print(_seek)
            else:
                print(_seek)
                already_send = int(_seek)
                pbar = processbar()
                with open(file_name,'rb') as f:
                    f.seek(int(_seek))
                    for line in f:
                        already_send +=len(line)
                        pbar.bar((already_send/length)*100)
                        self.conn.send(line)
                print('send over')
        else:
            print(flag.decode())




    def get(self,command):                                 #下载文件
        self.conn.send(command.encode('utf-8'))
        file_len = self.conn.recv(1024).decode()        #待收的文件大小
        print(file_len)
        file_name = command.strip().replace('get ', '').split('/').pop()
        if os.path.exists(file_name):
            _seek = os.stat(file_name).st_size
            mode = 'ab+'
        else:
            _seek =0
            mode = 'wb'
        self.conn.send(str(_seek).encode('utf-8'))
        length = int(file_len) - _seek                       #还剩多少要收的文件大小
        pbar = processbar()
        count =0
        with open(command.strip().replace('get ', ''), mode) as f:  # 写入文件
            while length >0 :       #当已收的文件大小<代收的文件大小，循环收取数据
                count +=1
                pbar.bar((1-length/int(file_len))*100)                  #传输进度条

                data = self.conn.recv(1024)
                length -= len(data)
                if data:
                    f.write(data)
                else:
                    exit()
                # print(body)
                # print('len',length)








# if __name__ == '__main__':
#     # karl = user('karl','123','/Users/karl_/Documents/GitHub/ftp/data/home/karl',0)
#     karl.connect('localhost',6967)
#
#     count = 3
#     while count >0:
#         name = input('name:')
#         passwd = getpass.getpass('passwd:')
#         if count == 0:
#             exit()
#         if karl.login(name,passwd):
#             while True:
#                 command = input('>>:')
#                 karl.exec_command(command)
#         else:
#             count -= 1
#             continue






