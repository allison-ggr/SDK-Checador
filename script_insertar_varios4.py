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
    {"id": 4001, "idE": 345, "nm": 'Espinoza Garcia Gamaliel', "pvg": "Admin", "id_checador": 40},
    {"id": 4002, "idE": 357, "nm": 'Romero Mancilla Luis Enrique', "pvg": "User", "id_checador": 40},
    {"id": 4003, "idE": 477, "nm": 'Nuñez Cruz Brianda Janeth', "pvg": "Admin", "id_checador": 40},
    {"id": 4004, "idE": 513, "nm": 'Baltazar Cortes Beatriz Mariela', "pvg": "User", "id_checador": 4},
    {"id": 4005, "idE": 625, "nm": 'Elizondo Guzman Karen Lizeth', "pvg": "User", "id_checador": 40},
    {"id": 4006, "idE": 646, "nm": 'Garcia Amezcua Ezequiel', "pvg": "User", "id_checador": 40},
    {"id": 4007, "idE": 746, "nm": 'Sosa Aguilar Karen Valeria', "pvg": "User", "id_checador": 40},
    {"id": 4008, "idE": 752, "nm": 'Gomez Alcaraz Valeria Betsabe', "pvg": "User", "id_checador": 40},
    {"id": 4009, "idE": 757, "nm": 'Cruz Ramirez Monica Lizbeth', "pvg": "User", "id_checador": 40},
    {"id": 4010, "idE": 756, "nm": 'Susana Lizbeth Jiménez Márquez', "pvg": "User", "id_checador": 40},
    {"id": 4011, "idE": 837, "nm": 'Gerardo Guzmán Chávez', "pvg": "User", "id_checador": 40},
    {"id": 4012, "idE": 838, "nm": 'Claudia Jiménez Méndez', "pvg": "User", "id_checador": 40},
    {"id": 4013, "idE": 839, "nm": 'Martin Mejía Hernández', "pvg": "User", "id_checador": 40},
    {"id": 4014, "idE": 837, "nm": 'Gearado Guzman Chavez', "pvg": "User", "id_checador": 40},
    {"id": 4015, "idE": 838, "nm": 'Claudia Alejandra Jimenez Mendez', "pvg": "User", "id_checador": 40},
    {"id": 4016, "idE": 848, "nm": 'Maria Antonia Sandoval Bernal', "pvg": "User", "id_checador": 40},
    {"id": 4017, "idE": 847, "nm": 'Alfonso Lopez Mendoza', "pvg": "User", "id_checador": 40},
    {"id": 4018, "idE": 9999, "nm": 'Ana Lilia Lopez Robles', "pvg": "User", "id_checador": 40},
    {"id": 4019, "idE": 874, "nm": 'Elizabeth Alejandro Chávez Morales', "pvg": "User", "id_checador": 40},
    {"id": 4020, "idE": 866, "nm": 'Jose Lopez Lopez', "pvg": "User", "id_checador": 40},
    {"id": 4021, "idE": 867, "nm": 'Erika Guadalupe Guzmán Rodríguez ', "pvg": "User", "id_checador": 40}
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