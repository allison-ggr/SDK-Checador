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
    {"id": 2001, "idE": 190, "nm": 'Guerrero Ramirez Alejandra Herminia', "pvg": "User", "id_checador": 20},
    {"id": 2002, "idE": 297, "nm": 'Anaya Campos Andrea', "pvg": "User", "id_checador": 20},
    {"id": 2003, "idE": 298, "nm": 'Martinez Lopez Christian Fabian', "pvg": "User", "id_checador": 20},
    {"id": 2004, "idE": 394, "nm": 'Amezcua Vargas Gerardo', "pvg": "User", "id_checador": 20},
    {"id": 2005, "idE": 456, "nm": 'Tavarez Reynoso Maria Leticia', "pvg": "User", "id_checador": 20},
    {"id": 2006, "idE": 594, "nm": 'Lopez Robles Ana Lilia', "pvg": "User", "id_checador": 20},
    {"id": 2007, "idE": 614, "nm": 'Parra Navarro Ena Maria Del  Carmen', "pvg": "Admin", "id_checador": 20},
    {"id": 2008, "idE": 741, "nm": 'Garcia Cortes Cesar Gabriel', "pvg": "User", "id_checador": 20},
    {"id": 2009, "idE": 742, "nm": 'Flores Arroyo Alfonso Gerardo', "pvg": "User", "id_checador": 20},
    {"id": 2010, "idE": 726, "nm": 'Maria Ramona Hernandez Hernandez', "pvg": "User", "id_checador": 20},
    {"id": 2011, "idE": 744, "nm": 'Torres Lopez Jose Luis', "pvg": "User", "id_checador": 20},
    {"id": 2012, "idE": 573, "nm": 'Alanez Carvajal Carlos Cesar', "pvg": "User", "id_checador": 20},
    {"id": 2013, "idE": 726, "nm": 'Maria Ramona Hernandez Hernandez', "pvg": "User", "id_checador": 20},
    {"id": 2014, "idE": 755, "nm": 'Delgado Gómez Noe Gabriel', "pvg": "User", "id_checador": 20},
    {"id": 2015, "idE": 753, "nm": 'Mendez Estrada Beatriz Amanda', "pvg": "User", "id_checador": 20},
    {"id": 2016, "idE": 758, "nm": 'Mara Sofia Rosales Barboza', "pvg": "User", "id_checador": 20},
    {"id": 2017, "idE": 753, "nm": 'Beatriz Amanda Mendez Estrada', "pvg": "User", "id_checador": 20},
    {"id": 2018, "idE": 758, "nm": 'Mara Sofia Rosales Barboza', "pvg": "User", "id_checador": 20},
    {"id": 2019, "idE": 762, "nm": 'Belen Guadalupe Hernandez Casillas', "pvg": "User", "id_checador": 20},
    {"id": 2020, "idE": 7, "nm": 'Alvaro Gomez Rodriguez', "pvg": "User", "id_checador": 20},
    {"id": 2021, "idE": 809, "nm": 'Ana Elizabeth Arroyo Lopez', "pvg": "User", "id_checador": 20},
    {"id": 2022, "idE": 772, "nm": 'Luis Enrique Ramirez Flores', "pvg": "User", "id_checador": 20},
    {"id": 2023, "idE": 744, "nm": 'Torrez Lopez Jose Luis', "pvg": "User", "id_checador": 20},
    {"id": 2024, "idE": 804, "nm": 'Torres Gonzalez Laura Yoselin', "pvg": "User", "id_checador": 20},
    {"id": 2025, "idE": 769, "nm": 'Virgen Mejia Irene', "pvg": "User", "id_checador": 20},
    {"id": 2026, "idE": 805, "nm": 'Islas Gonzalez Erika Janett', "pvg": "User", "id_checador": 20},
    {"id": 2027, "idE": 806, "nm": 'Nuñez Prado Ma. Isabel', "pvg": "User", "id_checador": 20},
    {"id": 2028, "idE": 801, "nm": 'Rivera Rubio Norma Noemi', "pvg": "User", "id_checador": 20},
    {"id": 2029, "idE": 813, "nm": 'Gloria Del Carmen Álvarez Diaz ', "pvg": "User", "id_checador": 20},
    {"id": 2030, "idE": 821, "nm": 'Blanca Elizabeth Torres Vazquez', "pvg": "User", "id_checador": 20},
    {"id": 2031, "idE": 823, "nm": 'Jose Gabriel Cortes Murillo', "pvg": "User", "id_checador": 20},
    {"id": 2032, "idE": 829, "nm": 'Elvia Olivia Zepeda Peña', "pvg": "User", "id_checador": 20},
    {"id": 2033, "idE": 828, "nm": 'Maria Guadalupe Guevara Cuevas', "pvg": "User", "id_checador": 20},
    {"id": 2034, "idE": 851, "nm": 'Raul Alejandro Perez Chitica', "pvg": "User", "id_checador": 20},
    {"id": 2035, "idE": 842, "nm": 'Sergio Agustin Fregoso Garcia', "pvg": "User", "id_checador": 20},
    {"id": 2036, "idE": 841, "nm": 'Maria del Carmen Prado Beltran ', "pvg": "User", "id_checador": 20},
    {"id": 2037, "idE": 846, "nm": 'Iliana Guadalupe Romero Gonzalez', "pvg": "User", "id_checador": 20},
    {"id": 2038, "idE": 853, "nm": 'Jocelyn Esperanza Mora Herrera', "pvg": "User", "id_checador": 20},
    {"id": 2039, "idE": 0, "nm": 'Leticia Victoria Lopez Hernandez ', "pvg": "User", "id_checador": 20},
    {"id": 2040, "idE": 859, "nm": 'Alejandra Medina Santillan', "pvg": "User", "id_checador": 20},
    {"id": 2041, "idE": 869, "nm": 'Abigail Guerrero Ramírez', "pvg": "User", "id_checador": 20},
    {"id": 2042, "idE": 876, "nm": 'Celia Guadalupe Chavez Mercado', "pvg": "User", "id_checador": 20},
    {"id": 2043, "idE": 859, "nm": 'Alejandra Medina Santillan', "pvg": "User", "id_checador": 20}
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