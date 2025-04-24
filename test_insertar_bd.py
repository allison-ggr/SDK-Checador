import argparse
from zk import ZK, const
import pymysql

# Configuración de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("id", type=int, help="ID y UID del usuario (deben ser iguales)")
parser.add_argument("idE", type=int, help="ID del empleado")
parser.add_argument("nm", type=str, help="Nombre del usuario")
parser.add_argument("pvg", type=str, choices=["User", "Admin"], help="Privilegio del usuario (User o Admin)")
parser.add_argument("ip", type=str, help="Dirección IP del dispositivo")
parser.add_argument("checador_id", type=int, help="ID del checador")
args = parser.parse_args()

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    # Conexión al dispositivo
    print("Conectando al dispositivo...")
    conn = zk.connect()
    print("Deshabilitando el dispositivo...")
    conn.disable_device()

    # Insertar usuario en el dispositivo
    privilege = const.USER_DEFAULT if args.pvg == "User" else const.USER_ADMIN
    conn.set_user(uid=args.id, name=args.nm, privilege=privilege, password='', group_id='', user_id=str(args.id), card=0)
    print(f"Usuario insertado en el dispositivo: ID/UID={args.id}, Nombre={args.nm}, Privilegio={args.pvg}")

    # Usar el archivo conexion.py para insertar en la base de datos
    print("Conectando a la base de datos...")
    conexion = pymysql.connect(
        host='192.168.1.175',
        user='authen',
        password='D3s@rr0ll02022',
        db='pruebaChecador'
    )
    try:
        with conexion.cursor() as cursor:
            # Insertar usuario en la base de datos
            consulta = """
                INSERT INTO empleados (id_usuario, id_empleado, nombre_completo, tipo, id_checador)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(consulta, (args.id, args.idE, args.nm, args.pvg, args.checador_id))
            conexion.commit()
            print(f"Usuario insertado en la base de datos: ID={args.id}, Nombre={args.nm}, Privilegio={args.pvg}, ID_Checador={args.checador_id}")
    finally:
        conexion.close()
        print("Conexión a la base de datos cerrada.")

    print("Habilitando el dispositivo...")
    conn.enable_device()
except Exception as e:
    print(f"Proceso terminado con error: {e}")
finally:
    if conn:
        conn.disconnect()