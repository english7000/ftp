#coding=utf-8
#！/usr/bin/env python3


import os,sys

class processbar(object):

    def __init__(self):
        pass


    def bar(self,process):          #process 取值1-100
        sys.stdout.write('\r')
        sys.stdout.write('%s%% :' % process +'*' * int(process/10))
        sys.stdout.flush()