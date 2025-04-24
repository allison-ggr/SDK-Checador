import argparse
from zk import ZK, const

# Configuración de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("id", type=int, help="ID y UID del usuario (deben ser iguales)")
parser.add_argument("nm", type=str, help="Nombre del usuario")
parser.add_argument("pvg", type=str, choices=["User", "Admin"], help="Privilegio del usuario (User o Admin)")
parser.add_argument("ip", type=str, help="Dirección IP del dispositivo")
args = parser.parse_args()

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    print("Conectando al dispositivo...")
    conn = zk.connect()
    print("Deshabilitando el dispositivo...")
    conn.disable_device()

    # Insertar usuario con ID y UID iguales
    privilege = const.USER_DEFAULT if args.pvg == "User" else const.USER_ADMIN
    conn.set_user(uid=args.id, name=args.nm, privilege=privilege, password='', group_id='', user_id=str(args.id), card=0)
    print(f"Usuario insertado: ID/UID={args.id}, Nombre={args.nm}, Privilegio={args.pvg}")

    print("Habilitando el dispositivo...")
    conn.enable_device()
except Exception as e:
    print(f"Proceso terminado con error: {e}")
finally:
    if conn:
        conn.disconnect()