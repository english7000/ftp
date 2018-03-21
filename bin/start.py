#coding=utf-8
#！/usr/bin/env python3

import sys
import os
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
from core import Main

Main.run()