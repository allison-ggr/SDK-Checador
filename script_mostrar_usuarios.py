# -*- coding: utf-8 -*-
import sys
import json
sys.path.append("zk")

from zk import ZK, const

conn = None
zk = ZK('192.168.1.200', port=4370, timeout=10, password=0, force_udp=False, ommit_ping=False)
try:
    print('Connecting to device ...')
    conn = zk.connect()
    print('Disabling device ...')
    conn.disable_device()

    users = conn.get_users()
    user_list = []

    for user in users:
        privilege = 'Admin' if user.privilege == const.USER_ADMIN else 'User'
        user_data = {
            "user_id": user.user_id,
            "nombre": user.name,
            "privilegio": privilege
        }
        user_list.append(user_data)

    # Imprimir como JSON formateado
    print(json.dumps(user_list, indent=4, ensure_ascii=False))

except Exception as e:
    print("Process terminated: {}".format(e))
finally:
    if conn:
        conn.disconnect()
