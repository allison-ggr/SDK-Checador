# -*- coding: utf-8 -*-
import sys
sys.path.append("zk")

from zk import ZK, const

conn = None
zk = ZK('192.168.1.200', port=4370, timeout=10, password=0, force_udp=False, ommit_ping=False)
try:

    print ('Connecting to device ...')
    conn = zk.connect()
    print ('Disabling device ...')
    conn.disable_device()
    
    users = conn.get_users()
    for user in users:
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        else:
            privilege = 'User'
        print ('ID: {}, Name: {}, Privilege: {}'.format(user.uid, user.name, privilege))

except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()

