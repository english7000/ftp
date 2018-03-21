#coding=utf-8
#！/usr/bin/env python3


import hashlib

with open('op.mp4','rb') as f:
    md5 = hashlib.md5()
    for line in f:

        md5.update(line)
    print(md5.hexdigest() )


with open('../../../core/op.mp4','rb') as f:
    md5_2 = hashlib.md5()
    for line in f:

        md5_2.update(line)
    print(md5_2.hexdigest() )