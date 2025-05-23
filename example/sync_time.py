# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK


conn = None
zk = ZK('192.168.1.200', port=4370)
try:
    conn = zk.connect()
    print ("Syncing time...")
    conn.set_time(datetime.now())
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
