import pymysql
from zk import ZK, const
from zk.finger import Finger
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("uid_usuarioAnterior", type=int, help="UID del usuario anterior (origen)")
parser.add_argument("uid_usuarioNuevo", type=int, help="UID del usuario nuevo (destino)")
parser.add_argument("nombre_usuarioNuevo", type=str, help="Nombre completo del nuevo usuario")
parser.add_argument("id_empleado", type=int, help="ID del empleado")
parser.add_argument("tipo", type=str, choices=["User", "Admin"], help="Privilegio del usuario (User o Admin)")
parser.add_argument("id_checador", type=int, help="ID del checador")
parser.add_argument("ip_checador", type=str, help="IP del checador")
args = parser.parse_args()

privilegio = const.USER_DEFAULT if args.tipo == "User" else const.USER_ADMIN

response = {}

# Conexión a la base de datos MySQL
db = pymysql.connect(
    host="192.168.1.175",
    user="authen",
    password="D3s@rr0ll02022",
    database="pruebaChecador"
)
cursor = db.cursor()

# Buscar todas las huellas de ese usuario
cursor.execute(
    "SELECT finger_id, template FROM huellas WHERE user_uid = %s AND id_checador = %s",
    (args.uid_usuarioAnterior, args.id_checador)
)
resultados = cursor.fetchall()

if resultados:
    # Conexión al reloj ZK
    zk = ZK(args.ip_checador, port=4370, timeout=30, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.disable_device()

    # Procesar el nombre para el checador
    nombre_completo = args.nombre_usuarioNuevo.strip().upper().split()
    primer_nombre = nombre_completo[0] if len(nombre_completo) > 0 else ""
    primer_apellido = ""
    inicial_segundo_apellido = ""

    if len(nombre_completo) == 2:
        primer_apellido = nombre_completo[1]
    elif len(nombre_completo) >= 3:
        primer_apellido = nombre_completo[-2]
        inicial_segundo_apellido = nombre_completo[-1][0]

    nombre_checador = f"{primer_nombre} {primer_apellido} {inicial_segundo_apellido}".strip()

    # Crear el usuario en el reloj
    conn.set_user(
        uid=args.uid_usuarioNuevo,
        name=nombre_checador,
        privilege=privilegio,
        password='',
        group_id='0',
        user_id=str(args.uid_usuarioNuevo)
    )
    response["dispositivo"] = {
        "status": "insertado",
        "id": args.uid_usuarioNuevo,
        "nombre": nombre_checador,
        "privilegio": args.tipo
    }

    # Crear las huellas (puede tener varias)
    fingers = []
    for finger_id, template_data in resultados:
        finger = Finger(
            uid=args.uid_usuarioNuevo,
            fid=finger_id,
            valid=1,
            template=template_data
        )
        fingers.append(finger)

    # Guardar todas las huellas del usuario
    conn.save_user_template(args.uid_usuarioNuevo, fingers)
    conn.enable_device()
    conn.disconnect()

    # Insertar usuario en la base de datos
    cursor.execute(
        "SELECT COUNT(*) FROM empleados WHERE id_usuario = %s",
        (args.uid_usuarioNuevo,)
    )
    existe = cursor.fetchone()
    if existe and existe[0] == 0:
        cursor.execute(
            """
            INSERT INTO empleados (id_usuario, id_empleado, nombre_completo, tipo, id_checador)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                args.uid_usuarioNuevo,
                args.id_empleado,
                args.nombre_usuarioNuevo.upper(),
                args.tipo,
                args.id_checador
            )
        )
        db.commit()
        response["base_datos"] = {
            "status": "insertado",
            "id": args.uid_usuarioNuevo,
            "nombre": args.nombre_usuarioNuevo.upper(),
            "privilegio": args.tipo,
            "id_empleado": args.id_empleado,
            "id_checador": args.id_checador
        }
    else:
        response["base_datos"] = {
            "status": "ya_existe",
            "id": args.uid_usuarioNuevo,
            "mensaje": f"El usuario {args.uid_usuarioNuevo} ya existe en la base de datos."
        }

    # Insertar/actualizar huellas en la base de datos para el nuevo usuario
    for finger_id, template_data in resultados:
        cursor.execute(
            "INSERT INTO huellas (user_uid, finger_id, template, id_checador) VALUES (%s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE template=VALUES(template)",
            (args.uid_usuarioNuevo, finger_id, template_data, args.id_checador)
        )
    db.commit()
    response["huellas"] = {
        "status": "insertadas",
        "total": len(resultados)
    }

else:
    response["error"] = f"No se encontraron huellas para el usuario {args.uid_usuarioAnterior} en el checador {args.id_checador}"

# Cerrar conexión a la base
cursor.close()
db.close()

print(json.dumps(response, indent=4))