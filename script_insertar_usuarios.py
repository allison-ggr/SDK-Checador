import argparse
import pymysql
import json
from zk import ZK, const

# Configuración de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("id", type=int, help="ID y UID del usuario (deben ser iguales)")
parser.add_argument("idE", type=int, help="ID del empleado")
parser.add_argument("nm", type=str, help="Nombre completo del usuario (Ejemplo: Juan Carlos Pérez López)")
parser.add_argument("pvg", type=str, choices=["User", "Admin"], help="Privilegio del usuario (User o Admin)")
parser.add_argument("ip", type=str, help="Dirección IP del dispositivo")
parser.add_argument("checador_id", type=int, help="ID del checador")
args = parser.parse_args()

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    response = {}
    conn = zk.connect()
    conn.disable_device()

    # Verificar si el usuario ya está registrado en el dispositivo
    usuarios_dispositivo = conn.get_users()
    usuario_existente = next((u for u in usuarios_dispositivo if u.uid == args.id), None)
    if usuario_existente:
        raise Exception(f"El usuario con ID {args.id} ya está registrado en el dispositivo.")

    # Procesar el nombre
    nombre_completo = args.nm.strip().upper().split()  # Convertir a mayúsculas y dividir
    primer_nombre = nombre_completo[0] if len(nombre_completo) > 0 else ""
    primer_apellido = ""
    inicial_segundo_apellido = ""

    # Manejar casos de nombres y apellidos
    if len(nombre_completo) == 2:  # Un nombre y un apellido
        primer_apellido = nombre_completo[1]
    elif len(nombre_completo) >= 3:  # Al menos un nombre y dos apellidos
        primer_apellido = nombre_completo[-2]
        inicial_segundo_apellido = nombre_completo[-1][0]  # Inicial del segundo apellido

    # Formatear el nombre para el checador
    nombre_checador = f"{primer_nombre} {primer_apellido} {inicial_segundo_apellido}".strip()

    # Insertar usuario en el dispositivo
    privilege = const.USER_DEFAULT if args.pvg == "User" else const.USER_ADMIN
    conn.set_user(uid=args.id, name=nombre_checador, privilege=privilege, password='', group_id='', user_id=str(args.id), card=0)
    response["dispositivo"] = {
        "status": "insertado",
        "id": args.id,
        "nombre": nombre_checador,
        "privilegio": args.pvg
    }

    # Conectar a la base de datos
    conexion = pymysql.connect(
        host='192.168.1.175',
        user='authen',
        password='D3s@rr0ll02022',
        db='pruebaChecador'
    )
    try:
        with conexion.cursor() as cursor:
            # Verificar si el usuario ya está registrado en la base de datos
            consulta_verificar = "SELECT COUNT(*) FROM empleados WHERE id_usuario = %s"
            cursor.execute(consulta_verificar, (args.id,))
            resultado = cursor.fetchone()
            if resultado[0] > 0:
                raise Exception(f"El usuario con ID {args.id} ya está registrado en la base de datos.")
            else:
                # Insertar usuario en la base de datos
                consulta_insertar = """
                    INSERT INTO empleados (id_usuario, id_empleado, nombre_completo, tipo, id_checador)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(consulta_insertar, (args.id, args.idE, args.nm.upper(), args.pvg, args.checador_id))  # Convertir a mayúsculas
                conexion.commit()
                response["base_datos"] = {
                    "status": "insertado",
                    "id": args.id,
                    "nombre": args.nm.upper(),
                    "privilegio": args.pvg,
                    "id_empleado": args.idE,
                    "id_checador": args.checador_id
                }
    finally:
        conexion.close()

    conn.enable_device()

    # Devolver respuesta en formato JSON
    print(json.dumps(response, indent=4))

except Exception:
    # Devolver JSON vacío en caso de error
    print(json.dumps({}))
finally:
    if conn:
        conn.disconnect()