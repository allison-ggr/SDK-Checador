import pymysql
from zk import ZK, const
from zk.finger import Finger

# Conexión a la base de datos MySQL
db = pymysql.connect(
    host="192.168.1.175",           # o la IP del servidor MySQL
    user="authen",                 # tu usuario de MySQL
    password="D3s@rr0ll02022",      # tu contraseña
    database="pruebaChecador" # tu base de datos
)

cursor = db.cursor()

# UID del usuario que quieres restaurar
uid_usuario = 1228

# Buscar todas las huellas de ese usuario
cursor.execute("SELECT finger_id, template FROM huellas WHERE user_uid = %s", (uid_usuario,))
resultados = cursor.fetchall()

if resultados:
    # Conexión al reloj ZK
    zk = ZK('192.168.1.200', port=4370, timeout=30, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.disable_device()

    # Crear el usuario en el reloj
    conn.set_user(
        uid=uid_usuario,
        name=f'MeniquePrueba2',  # Aquí puedes ponerle un nombre real si quieres
        privilege=const.USER_ADMIN,
        password='',
        group_id='0',
        user_id=str(uid_usuario)
    )
    print(f"Usuario {uid_usuario} creado.")

    # Crear las huellas (puede tener varias)
    fingers = []
    for finger_id, template_data in resultados:
        finger = Finger(
            uid=uid_usuario,
            fid=finger_id,
            valid=1,
            template=template_data
        )
        fingers.append(finger)

    # Guardar todas las huellas del usuario
    conn.save_user_template(uid_usuario, fingers)
    print("Huellas restauradas exitosamente.")

    # Finalizar conexión
    conn.enable_device()
    conn.disconnect()

else:
    print(f"No se encontraron huellas para el usuario {uid_usuario}")

# Cerrar conexión a la base
cursor.close()
db.close()
