# -*- coding: utf-8 -*-
import sys
import json
import argparse

sys.path.append("zk")

from zk import ZK, const

# Argumentos
parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str, help="IP del checador")
args = parser.parse_args()

# Conexión al checador
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
conn = None

try:
    conn = zk.connect()
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

    print(json.dumps(user_list, indent=4, ensure_ascii=False))

except Exception as e:
    print(json.dumps([], ensure_ascii=False))  # Devuelve lista vacía como JSON

finally:
    if conn:
        conn.disconnect()
