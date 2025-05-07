import argparse
import pymysql
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
print("Conexión exitosa a la base de datos.")

# Conexión al checador
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
conn = None

try:
    conn = zk.connect()
    conn.disable_device()

    # Eliminar usuario del checador
    conn.delete_user(user_id=args.id)
    print(f"Usuario con ID {args.id} eliminado del checador.")

    # Eliminar usuario de la base de datos
    cursor.execute("DELETE FROM huellasrespaldo WHERE id_usuario = %s", (args.id,))
    cursor.execute("DELETE FROM empleados WHERE id_usuario = %s", (args.id,))

    # Verificación y commit
    cursor.execute("SELECT COUNT(*) FROM huellasrespaldo WHERE id_usuario = %s", (args.id,))
    resultado = cursor.fetchone()
    if resultado[0] == 0:
        conexion.commit()
        print("Verificación exitosa: el usuario ya no está en la base de datos.")
    else:
        conexion.rollback()
        print("Error: el usuario aún existe en la base de datos. Cambios revertidos.")

except Exception as e:
    conexion.rollback()
    print(f"Proceso terminado con error: {e}")

finally:
    if conn:
        conn.disconnect()
    cursor.close()
    conexion.close()
