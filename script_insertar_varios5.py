import argparse
from zk import ZK, const
import pymysql

# Configuración de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str, help="Dirección IP del dispositivo")
args = parser.parse_args()

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

# Lista de usuarios a insertar
usuarios = [
    {"id": 5001, "idE": 593, "nm": 'Enrique Ayipey Villaseñor Rodriguez', "pvg": "User", "id_checador": 50},
    {"id": 5002, "idE": 149, "nm": 'Valeria Chantal Rayas Hernandez', "pvg": "Admin", "id_checador": 50},
    {"id": 5003, "idE": 583, "nm": 'Evelyn Vianey Valencia Valle', "pvg": "Admin", "id_checador": 50},
    {"id": 5004, "idE": 611, "nm": 'Karla Maria Jannet Carranza Guzman', "pvg": "Admin", "id_checador": 50},
    {"id": 5005, "idE": 0, "nm": 'Rodriguez Ruiz Melchor', "pvg": "User", "id_checador": 50}
    ]

try:
    # Conexión al dispositivo
    print("Conectando al dispositivo...")
    conn = zk.connect()
    print("Deshabilitando el dispositivo...")
    conn.disable_device()

    # Conexión a la base de datos
    print("Conectando a la base de datos...")
    conexion = pymysql.connect(
        host='192.168.1.175',
        user='authen',
        password='D3s@rr0ll02022',
        db='pruebaChecador'
    )

    try:
        with conexion.cursor() as cursor:
            for usuario in usuarios:
                # Insertar usuario en el dispositivo
                privilege = const.USER_DEFAULT if usuario["pvg"] == "User" else const.USER_ADMIN
                conn.set_user(uid=usuario["id"], name=usuario["nm"], privilege=privilege, password='', group_id='', user_id=str(usuario["id"]), card=0)
                print(f"Usuario insertado en el dispositivo: ID/UID={usuario['id']}, Nombre={usuario['nm']}, Privilegio={usuario['pvg']}")

                # Insertar usuario en la base de datos
                consulta = """
                    INSERT INTO empleados (id_usuario, id_empleado, nombre_completo, tipo, id_checador)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(consulta, (usuario["id"], usuario["idE"], usuario["nm"], usuario["pvg"], args.checador_id))
                conexion.commit()
                print(f"Usuario insertado en la base de datos: ID={usuario['id']}, Nombre={usuario['nm']}, Privilegio={usuario['pvg']}, ID_Checador={args.checador_id}")

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