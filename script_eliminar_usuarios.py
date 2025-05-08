import argparse
import pymysql
import json
from zk import ZK

# Argumentos
parser = argparse.ArgumentParser()
parser.add_argument("id", type=int, help="ID del usuario a eliminar")
parser.add_argument("ip", type=str, help="IP del reloj checador")
args = parser.parse_args()

# Conexión a la base de datos
conexion = pymysql.connect(
    host='192.168.1.175',
    user='authen',
    password='D3s@rr0ll02022',
    database='pruebaChecador'
)
cursor = conexion.cursor()

# Conexión al checador
zk = ZK(args.ip, port=4370, timeout=10, password=0, force_udp=False, ommit_ping=False)
conn = None

try:
    response = {}
    conn = zk.connect()
    conn.disable_device()

    # Verificar si el usuario existe en el checador
    usuarios_dispositivo = conn.get_users()
    usuario_existente = next((u for u in usuarios_dispositivo if int(u.user_id) == args.id), None)
    if not usuario_existente:
        raise Exception(f"El usuario con ID {args.id} no existe en el dispositivo.")

    # Eliminar usuario del checador
    conn.delete_user(user_id=args.id)
    response["dispositivo"] = {
        "status": "eliminado",
        "id": args.id
    }

    # Verificar si el usuario existe en la base de datos
    cursor.execute("SELECT COUNT(*) FROM empleados WHERE id_usuario = %s", (args.id,))
    resultado = cursor.fetchone()
    if resultado[0] == 0:
        raise Exception(f"El usuario con ID {args.id} no existe en la base de datos.")

    # Eliminar usuario de la base de datos
    cursor.execute("DELETE FROM huellasrespaldo WHERE id_usuario = %s", (args.id,))
    cursor.execute("DELETE FROM empleados WHERE id_usuario = %s", (args.id,))

    # Verificación y commit
    cursor.execute("SELECT COUNT(*) FROM huellasrespaldo WHERE id_usuario = %s", (args.id,))
    resultado = cursor.fetchone()
    if resultado[0] == 0:
        conexion.commit()
        response["base_datos"] = {
            "status": "eliminado",
            "id": args.id
        }
    else:
        conexion.rollback()
        raise Exception("Error: el usuario aún existe en la base de datos. Cambios revertidos.")

    conn.enable_device()

    # Devolver respuesta en formato JSON
    print(json.dumps(response, indent=4))

except Exception:
    # Devolver JSON vacío en caso de error
    print(json.dumps({}))
finally:
    if conn:
        conn.disconnect()
    cursor.close()
    conexion.close()