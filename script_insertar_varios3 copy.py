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
    {"id": 3001, "idE": 37, "nm": 'Torres Muñoz Jose De Jesus', "pvg": "Admin", "id_checador": 30},
    {"id": 3002, "idE": 117, "nm": 'Sanchez Carrillo Luz Maria', "pvg": "User", "id_checador": 30},
    {"id": 3003, "idE": 247, "nm": 'Islas Villanueva Antonia', "pvg": "User", "id_checador": 30},
    {"id": 3004, "idE": 325, "nm": 'Garcia Serna Norma Alejandra', "pvg": "User", "id_checador": 30},
    {"id": 3005, "idE": 388, "nm": 'Rodriguez Plazola Sandra', "pvg": "User", "id_checador": 30},
    {"id": 3006, "idE": 707, "nm": 'Sandoval Palomino Brenda Adriana', "pvg": "Admin", "id_checador": 30},
    {"id": 3007, "idE": 713, "nm": 'Escobedo Castro Patricia', "pvg": "User", "id_checador": 30},
    {"id": 3008, "idE": 716, "nm": 'Vazquez Gazcon Karla Noemi', "pvg": "Admin", "id_checador": 30},
    {"id": 3009, "idE": 743, "nm": 'Ceballos Baltazar Brenda Jacqueline', "pvg": "User", "id_checador": 3},
    {"id": 3010, "idE": 36, "nm": 'Rodriguez Ramirez Claudia', "pvg": "User", "id_checador": 30},
    {"id": 3011, "idE": 544, "nm": 'Ramirez Hernandez Pablo Michel', "pvg": "User", "id_checador": 30},
    {"id": 3012, "idE": 700, "nm": 'Avalos Sanchez Stefhania', "pvg": "User", "id_checador": 30},
    {"id": 3013, "idE": 733, "nm": 'Curiel Patiño Jesus Emmanuel', "pvg": "User", "id_checador": 30},
    {"id": 3014, "idE": 802, "nm": 'Claudia Elena Arias Medina ', "pvg": "User", "id_checador": 30},
    {"id": 3015, "idE": 814, "nm": 'Yatana Yazmín Xicoténcatl Castellanos ', "pvg": "User", "id_checador": 30},
    {"id": 3016, "idE": 815, "nm": 'María Del Rosario Ramírez Hernández ', "pvg": "User", "id_checador": 30},
    {"id": 3017, "idE": 871, "nm": 'Luis Oscar Daniel Huerta Torres', "pvg": "User", "id_checador": 30},
    {"id": 3018, "idE": 822, "nm": 'Mariana Gabriela Arreola Moreno', "pvg": "User", "id_checador": 30},
    {"id": 3019, "idE": 833, "nm": 'Maria del Carmen Ceja Avila', "pvg": "User", "id_checador": 30},
    {"id": 3020, "idE": 191, "nm": 'Lesli Janette Lopez Martin', "pvg": "User", "id_checador": 30},
    {"id": 3021, "idE": 843, "nm": 'Jesus Ivan Rivera Lucio', "pvg": "User", "id_checador": 30},
    {"id": 3022, "idE": 844, "nm": 'Arturo Perez Rodriguez', "pvg": "User", "id_checador": 30},
    {"id": 3023, "idE": 864, "nm": 'Carmen Felicitas Estrella Corral', "pvg": "User", "id_checador": 30},
    {"id": 3024, "idE": 872, "nm": 'Fátima Sagrario Rosas Martinez', "pvg": "User", "id_checador": 30},
    {"id": 3025, "idE": 875, "nm": 'Efrén Eduardo Castellanos Gutierrez', "pvg": "User", "id_checador": 30}
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