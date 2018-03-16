#coding=utf-8
#！/usr/bin/env python3


import os
import  socket

class user(object):
    '''用户类'''


    def __init__(self,name,passwd,homedir,quote):
        self.name = name
        self.passwd = passwd
        self.homedir = homedir
        self.conn =''
        self.quote = quote            #配额

    def login(self,name,passwd):
        self.conn.send(bytes(name,encoding='utf-8'))

        name_check = self.conn.recv(1024)
        if name_check == b'ok':
            self.conn.send(bytes(passwd,encoding='utf-8'))
            passwd_check = self.conn.recv(1024)
            if passwd_check ==b'ok':
                print('welcone back! %s' %name)
                print(self.conn.recv(1024).decode())
                return 1                            #认证成功
            else:
                print('Wrong passwd!')
                return 0

        else:
            print('no username :' ,name)
            return 0                                #认证失败



    def connect(self,ip,port):
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
        self.conn.send(command.encode('utf-8'))                   #fa
        self.conn.recv(1024)
        body = ''
        with open(command.strip().replace('put ',''),'r') as f:
            for line in f:
                body += line
        self.conn.send(str(len(body)).encode('utf-8'))
        data = self.conn.recv(1024)
        print(data)
        print(body)
        if data.decode() == 'ready':
            self.conn.send(body.encode('utf-8'))
            print('send over')
        else:
            pass


    def get(self,command):                                 #下载文件
        self.conn.send(command.encode('utf-8'))
        file_len = self.conn.recv(1024).decode()        #待收的文件大小
        self.conn.send(b'ready')
        length = 0                          #已收的文件大小
        body = ''
        count =0
        while length < int(file_len):       #当已收的文件大小<代收的文件大小，循环收取数据
            count +=1
            print(count)
            data = self.conn.recv(1024).decode()
            body += data
            length = len(body)
            print(body)
            print('len',length)

        with open(command.strip().replace('get ',''),'w') as f:         #写入文件
            f.write(body)





if __name__ == '__main__':
    karl = user('karl','123','/Users/karl_/Documents/GitHub/ftp/cfg',0)
    karl.connect('localhost',6965)

    count = 3
    while count >0:
        name = input('name:')
        passwd = input('passwd:')
        if count == 0:
            exit()
        if karl.login(name,passwd):
            while True:
                command = input('>>:')
                karl.exec_command(command)
        else:
            count -= 1
            continue






