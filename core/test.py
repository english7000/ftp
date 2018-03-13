#coding=utf-8
#！/usr/bin/env python3


import os
command = 'get aaa'
file_name = command.replace('get ','').split('/').pop()
print(file_name)