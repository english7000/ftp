#coding=utf-8
#！/usr/bin/env python3


import socketserver
import os
import pickle


class Myserver(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        print(self.client_address)
        '''先接收username和passwd对用户进行验证'''
        count= 3
        while count >=0:
            if count == 0:
                conn.close()
                exit()
            user_name = conn.recv(1024).strip().decode()
            user_info = self.init(user_name)
            # print(user_info)
            if user_info:
                conn.send(b'ok')
                user_passwd = conn.recv(1024).strip().decode()
                auth_res =self.auth(user_name,user_passwd,user_info)              #如果init有返回说明用户名存在然后调用auth方法来认证
                if auth_res:
                    conn.send(b'ok')
                    break
                else:
                    conn.send(b'failiure')
                    count -= 1
                    continue
            else:
                conn.send(b'failure')
                count -= 1
                continue

        used = int(os.popen("du -k %s | awk '{print $1}'"% user_info['homedir']).read())*1024
        os.chdir(user_info['homedir'])
        print(os.system('pwd'))

        useage = 'quota: %s used %s  available: %s   byte' %(str(user_info['quota']), str(used),str(int(user_info['quota'])- used))
        conn.send(useage.encode('utf-8'))
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

            elif command.strip().startswith('cd'):                      #假装实现
                path = command.strip().replace('cd ','')
                dir_check =os.popen('cd %s && pwd' % path).read()
                if dir_check.startswith(user_info['homedir']):
                    os.chdir(path)
                    conn.send(b'0')
                else:
                    conn.send(b'0')
                    continue

            elif command.strip().startswith('put'):                 #上传
                if int(user_info['quota']) > used:
                    file_name = command.replace('put ', '').split('/').pop()
                    print(file_name)
                    if os.path.exists(file_name):
                        _seek = os.stat(file_name).st_size
                        mode = 'ab+'
                    else:
                        _seek = 0
                        mode = 'wb'
                    conn.send(b'ok')
                    file_len = int(conn.recv(1024).decode())
                    print(file_len)
                    if file_len + used <= int(user_info['quota']):
                        conn.send(bytes(str(_seek),encoding='utf-8'))
                        length =int(file_len)-_seek
                        print(length)
                        with open(file_name, mode) as f:
                            while length >0:
                                data = conn.recv(1024)
                                length -= len(data)
                                # print(str((file_len - length/file_len)*100))
                                # os.system('clear')
                                if not data:
                                    break
                                f.write(data)
                    else:
                        conn.send(b'no space left')
                else:
                    conn.send(b'no spqce left')

            elif command.strip().startswith('get'):                 #下载
                file_name = command.replace('get ', '').split('/').pop()
                print(file_name)
                length = int(os.popen("ls -l %s |awk '{print $5}' " % file_name).read())
                conn.send(str(length).encode('utf-8'))
                _seek = conn.recv(1024).decode()
                with open(file_name,'rb') as f:
                    f.seek(int(_seek))
                    for line in f :
                        conn.send(line)
                print('\n\+''send over')




    @staticmethod                   #设置认证的静态方法
    def auth(name,passwd,user_info):
        if user_info['name'] == name and user_info['passwd'] == passwd:
            print('Welcome back! %s'% name)
            return 1
        else:
            print('Username or passwd wrong!')
            return 0

    @staticmethod                   #设置初始化的静态方法
    def init(name):                 #读取相应的用户字典user_info
        user_info ={}
        os.chdir('/Users/karl_/Documents/GitHub/ftp/core')              #多线程登录时由于有chdir命令导致第二次登录会找不到账户文件所以要chdir回来
        try:
            with open('../data/user_info/%s' % name,'rb')as f:
                user_info = pickle.load(f)
                # print('-----',user_info)
            return user_info
        except Exception as e :                    #验证用户是否存在，不存在则显示NO user
            print(e)
            return 0






if __name__ == '__main__':


    # karl ={'name':'karl','passwd':'123','quota':'100000000','homedir':'../data/home/karl'}
    # with open('../data/user_info/karl','wb') as f:
    #     pickle.dump(karl,f)

    server = socketserver.ThreadingTCPServer(('localhost', 6967), Myserver)  # 直接多线程实例化
    server.serve_forever()

    # karl = Myserver.init('karl')
    # print(karl)




