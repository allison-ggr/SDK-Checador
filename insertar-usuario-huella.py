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


uid_usuarioAnterior = 8
uid_usuarioNUevo = 105
nombre_usuarioNuevo = 'TERESA DE JESUS ROMERO' # Nombre del nuevo usuario (puedes cambiarlo si quieres)
privilegio = const.USER_DEFAULT  # Privilegio de usuario normal


# Buscar todas las huellas de ese usuario
cursor.execute("SELECT finger_id, template FROM huellas WHERE user_uid = %s", (uid_usuarioAnterior,))
resultados = cursor.fetchall()

if resultados:
    # Conexión al reloj ZK
    zk = ZK('192.168.1.200', port=4370, timeout=30, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.disable_device()

    # Crear el usuario en el reloj
    conn.set_user(
        uid=uid_usuarioNUevo,
        name=nombre_usuarioNuevo,  # Aquí puedes ponerle un nombre real si quieres
        privilege=privilegio,
        password='',
        group_id='0',
        user_id=str(uid_usuarioNUevo)
    )
    print(f"Usuario {uid_usuarioNUevo} creado.")

    # Crear las huellas (puede tener varias)
    fingers = []
    for finger_id, template_data in resultados:
        finger = Finger(
            uid=uid_usuarioNUevo,
            fid=finger_id,
            valid=1,
            template=template_data
        )
        fingers.append(finger)

    # Guardar todas las huellas del usuario
    conn.save_user_template(uid_usuarioNUevo, fingers)
    print("Huellas restauradas exitosamente.")
    conn.delete_user(uid_usuarioAnterior)  # Eliminar el usuario anterior del reloj
    print(f"Usuario {uid_usuarioAnterior} eliminado.")
    # Finalizar conexión
    conn.enable_device()
    conn.disconnect()

else:
    print(f"No se encontraron huellas para el usuario {uid_usuarioNUevo}")

# Cerrar conexión a la base
cursor.close()
db.close()
