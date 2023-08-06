#!/usr/bin/env python
import datetime
import json
from typing import Dict, List, Optional, Set, Tuple

import sys ,os 
import requests


def dbinstall():
    cmd = 'pip3 install {} -i https://pypi.douban.com/simple'.format(' '.join(sys.argv[1:]))
    os.system(cmd)

def syncfile():
    file = sys.argv[1]
    try:
        cmd = f"curl -s file.ddot.cc/gofil|bash -s {file}"
        resp = os.system(cmd)
        print(resp)
    except FileNotFoundError as e:
        print(e)

def esyncfile():
    """sync file with encryption"""
    file = sys.argv[1]
    try:
        cmd = f"curl -s file.ddot.cc/gofile|bash -s {file}"
        resp = os.system(cmd)
        print(resp)
    except FileNotFoundError as e:
        print(e)



