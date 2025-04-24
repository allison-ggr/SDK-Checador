# -*- coding: utf-8 -*-
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("id", type = str)
args = parser.parse_args()

sys.path.append("zk")

from zk import ZK, const

conn = None
zk = ZK('192.168.1.200', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    print ('Connecting to device ...')
    conn = zk.connect()
    print ('Disabling device ...')
    conn.disable_device()
    print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
    # print '--- Get User ---'
    users = conn.get_users()
    finger = conn.get_user_template()
    
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        if user.user_id == args.id:
            print ('  UID      : {}'.format(user.uid))
    
    print ('Enabling device ...')
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()