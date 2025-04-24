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
    {"id": 1001, "idE": 10, "nm": "Guzman Tatengo Ivan Raymundo", "pvg": "User", "id_checador": 10},
    {"id": 1002, "idE": 460, "nm": "Martinez Rodriguez Miriam Rossana", "pvg": "User", "id_checador": 10},
    {"id": 1003, "idE": 278, "nm": "Rodriguez Lomeli Arnoldo", "pvg": "User", "id_checador": 10},
    {"id": 1004, "idE": 673, "nm": "Garcia Barrera Daniela Montserrat", "pvg": "User", "id_checador": 10},
    {"id": 1005, "idE": 570, "nm": "Jimenez Castañeda Miriam Liliana", "pvg": "User", "id_checador": 10},
    {"id": 1006, "idE": 252, "nm": "Palacios Casasola Edwin Eduardo", "pvg": "User", "id_checador": 10},
    {"id": 1007, "idE": 541, "nm": "Flores De Jesus Ana Rosa", "pvg": "User", "id_checador": 10},
    {"id": 1008, "idE": 556, "nm": 'Parra Marquez Blanca Janeth', "pvg": "User", "id_checador": 10},
    {"id": 1009, "idE": 29, "nm": 'Romero Rodriguez Teresa De Jesus', "pvg": "User", "id_checador": 10},
    {"id": 1010, "idE": 498, "nm": 'Isordia Moreno Eduwiges', "pvg": "Admin", "id_checador": 10},
    {"id": 1011, "idE": 393, "nm": 'Gonzalez Castillo Ana Ilse', "pvg": "User", "id_checador": 10},
    {"id": 1012, "idE": 17, "nm": 'Negrete Hueso Joel Humberto', "pvg": "User", "id_checador": 10},
    {"id": 1013, "idE": 611, "nm": 'Carranza Guzman Karla Maria Jannet', "pvg": "Admin", "id_checador": 10},
    {"id": 1014, "idE": 286, "nm": 'Martinez Santiago Luis Alberto', "pvg": "User", "id_checador": 10},
    {"id": 1015, "idE": 735, "nm": 'Ayala Hernandez Eva Consepcion', "pvg": "User", "id_checador": 10},
    {"id": 1016, "idE": 709, "nm": 'Lares Illescas Alexander', "pvg": "User", "id_checador": 10},
    {"id": 1017, "idE": 0, "nm": 'Diaz Aguilar Jose Antonio', "pvg": "User", "id_checador": 10},
    {"id": 1018, "idE": 27, "nm": 'Rivas Marquez Yagaira', "pvg": "User", "id_checador": 10},
    {"id": 1019, "idE": 421, "nm": 'Rodriguez Ruiz Melchor', "pvg": "User", "id_checador": 10},
    {"id": 1020, "idE": 482, "nm": 'Hernandez Perez Esmeralda', "pvg": "User", "id_checador": 10},
    {"id": 1021, "idE": 736, "nm": 'Pacas Espinoza Elizabeth', "pvg": "User", "id_checador": 10},
    {"id": 1023, "idE": 555, "nm": 'Gutierrez Siordia Ana Karen', "pvg": "User", "id_checador": 10},
    {"id": 1024, "idE": 550, "nm": 'Gonzalez Naranjo Elizabeth', "pvg": "User", "id_checador": 10},
    {"id": 1025, "idE": 747, "nm": 'Cárdenas Angel Erick Javier', "pvg": "User", "id_checador": 10},
    {"id": 1026, "idE": 748, "nm": 'Lango Juan Martín Eugenio', "pvg": "User", "id_checador": 10},
    {"id": 1027, "idE": 749, "nm": 'Flores Montes Pedro Emmanuel', "pvg": "User", "id_checador": 10},
    {"id": 1028, "idE": 750, "nm": 'Jimenez Ramos German', "pvg": "User", "id_checador": 10},
    {"id": 1029, "idE": 754, "nm": 'Milagros Yessica Ortiz Zuñiga', "pvg": "User", "id_checador": 10},
    {"id": 1030, "idE": 760, "nm": 'Omar Alonso De Leon Mora', "pvg": "User", "id_checador": 10},
    {"id": 1031, "idE": 761, "nm": 'Nuñez Covarrubias Jorge Luis', "pvg": "User", "id_checador": 10},
    {"id": 1032, "idE": 764, "nm": 'Garcia Hernandez Jeyeli', "pvg": "User", "id_checador": 10},
    {"id": 1033, "idE": 0, "nm": 'Banda Jimenez Sandra Elizabeth', "pvg": "User", "id_checador": 10},
    {"id": 1034, "idE": 575, "nm": 'Aparicio Gonzalez Daniel', "pvg": "Admin", "id_checador": 10},
    {"id": 1035, "idE": 712, "nm": 'Salazar Vega Joaquin', "pvg": "Admin", "id_checador": 10},
    {"id": 1036, "idE": 722, "nm": 'Rodriguez Gutierrez Luis Manuel', "pvg": "User", "id_checador": 10},
    {"id": 1037, "idE": 778, "nm": 'Cardenas Alvarado Rodrigo Daniel', "pvg": "User", "id_checador": 10},
    {"id": 1038, "idE": 7, "nm": 'Alvaro Gomez Rodriguez', "pvg": "User", "id_checador": 10},
    {"id": 1039, "idE": 800, "nm": 'Jose Francisco Rodriguez Hernandez', "pvg": "User", "id_checador": 10},
    {"id": 1040, "idE": 654, "nm": 'Norma Galilea Palacios Casasola ', "pvg": "User", "id_checador": 10},
    {"id": 1041, "idE": 766, "nm": 'Xocoyotzin Javier Anguiano Garcia', "pvg": "User", "id_checador": 10},
    {"id": 1042, "idE": 767, "nm": 'García Vargas Victor Manuel', "pvg": "User", "id_checador": 10},
    {"id": 1043, "idE": 775, "nm": 'Gustavo Luján Flores', "pvg": "User", "id_checador": 10},
    {"id": 1044, "idE": 773, "nm": 'Juan Omar Mazahua Huerta', "pvg": "User", "id_checador": 10},
    {"id": 1045, "idE": 685, "nm": 'Rodriguez Pacas Maria Ahilin', "pvg": "User", "id_checador": 10},
    {"id": 1046, "idE": 807, "nm": 'Delgado Tejeda Georgina', "pvg": "User", "id_checador": 10},
    {"id": 1047, "idE": 810, "nm": 'Griselda Arevalo Rodriguez', "pvg": "User", "id_checador": 10},
    {"id": 1048, "idE": 816, "nm": 'Brenda Guadalupe Hernández Huerta ', "pvg": "User", "id_checador": 10},
    {"id": 1049, "idE": 818, "nm": 'Dalia Esmeralda Gallardo Gutierrez', "pvg": "User", "id_checador": 10},
    {"id": 1050, "idE": 819, "nm": 'Ana Cecilia Garcia Guzman', "pvg": "User", "id_checador": 10},
    {"id": 1051, "idE": 820, "nm": 'Imelda Vazquez Gonzalez', "pvg": "User", "id_checador": 10},
    {"id": 1052, "idE": 824, "nm": 'Juan Carlos Rodriguez Rodriguez', "pvg": "User", "id_checador": 10},
    {"id": 1053, "idE": 825, "nm": 'Carlos Mercado Mendez', "pvg": "User", "id_checador": 10},
    {"id": 1054, "idE": 573, "nm": 'Carlos Cesar Alanez Carvajal', "pvg": "User", "id_checador": 10},
    {"id": 1055, "idE": 900, "nm": 'Karla Carranza', "pvg": "User", "id_checador": 10},
    {"id": 1056, "idE": 827, "nm": 'Daniel Isaac Valdez Ceniceros', "pvg": "User", "id_checador": 10},
    {"id": 1057, "idE": 149, "nm": 'Valeria Chantal Rayas Hernandez', "pvg": "User", "id_checador": 10},
    {"id": 1058, "idE": 830, "nm": 'De la Torre Nava Ruben', "pvg": "Admin", "id_checador": 10},
    {"id": 1059, "idE": 831, "nm": 'Kenia Fernanda Godinez Garcia', "pvg": "User", "id_checador": 10},
    {"id": 1060, "idE": 836, "nm": 'Jiovanni Ureña Lopez', "pvg": "User", "id_checador": 10},
    {"id": 1061, "idE": 850, "nm": 'Roberto Gomez Duran', "pvg": "User", "id_checador": 10},
    {"id": 1062, "idE": 841, "nm": 'Maria del Carmen Prado Beltran', "pvg": "User", "id_checador": 10},
    {"id": 1063, "idE": 852, "nm": 'Alonso Gutiérrez Ernesto', "pvg": "Admin", "id_checador": 10},
    {"id": 1064, "idE": 842, "nm": 'Sergio Agustin Fregoso Garcia', "pvg": "User", "id_checador": 10},
    {"id": 1065, "idE": 856, "nm": 'Cynthia Guadalupe Duran Canales', "pvg": "User", "id_checador": 10},
    {"id": 1066, "idE": 857, "nm": 'Celia Nydia Sánchez Rodríguez ', "pvg": "User", "id_checador": 10},
    {"id": 1067, "idE": 858, "nm": 'José Michael Gutiérrez Ramírez ', "pvg": "User", "id_checador": 10},
    {"id": 1068, "idE": 863, "nm": 'Coreisy Cabrera Rodriguez', "pvg": "User", "id_checador": 10},
    {"id": 1069, "idE": 870, "nm": 'Erika Georgina Luna Guzman', "pvg": "User", "id_checador": 10},
    {"id": 1070, "idE": 874, "nm": 'Miriam Jazmín Vélez Ortiz ', "pvg": "User", "id_checador": 10},
    {"id": 1071, "idE": 866, "nm": 'Jose Lopez Lopez', "pvg": "User", "id_checador": 10}
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