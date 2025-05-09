import pymysql
import sys
import argparse
import json
sys.path.append("zk")
from zk import ZK, const

# Configuración de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str, help="Dirección IP del dispositivo checador")
args = parser.parse_args()

# Configuración del reloj checador
checador = ZK(args.ip, port=4370, timeout=20, password=0, force_udp=False, ommit_ping=False)

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": "192.168.1.175",       # Dirección del servidor MySQL
    "user": "authen",            # Usuario de MySQL
    "password": "D3s@rr0ll02022",  # Contraseña de MySQL
    "database": "pruebaChecador"  # Nombre de la base de datos
}

def inicializar_base_datos():
    """Crea las tablas necesarias en la base de datos si no existen."""
    conexion = pymysql.connect(**DB_CONFIG)
    try:
        with conexion.cursor() as cursor:
            # Crear tabla de usuarios
            cursor.execute('''  
                CREATE TABLE IF NOT EXISTS usuarios (
                    uid INT PRIMARY KEY,
                    user_id VARCHAR(50),
                    name VARCHAR(100),
                    privilege VARCHAR(20),
                    password VARCHAR(50),
                    group_id VARCHAR(50)
                )
            ''')

            # Crear tabla de huellas digitales
            cursor.execute('''  
                CREATE TABLE IF NOT EXISTS huellas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_uid INT,
                    finger_id INT,
                    template BLOB,
                    FOREIGN KEY (user_uid) REFERENCES usuarios (uid)
                )
            ''')

        conexion.commit()
    finally:
        conexion.close()

def guardar_en_base_datos(usuarios):
    """Guarda la información de los usuarios y sus huellas en la base de datos."""
    conexion = pymysql.connect(**DB_CONFIG)
    try:
        with conexion.cursor() as cursor:
            for user in usuarios:
                # Insertar o actualizar usuario
                cursor.execute('''  
                    INSERT INTO usuarios (uid, user_id, name, privilege, password, group_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    user_id=VALUES(user_id), name=VALUES(name), privilege=VALUES(privilege),
                    password=VALUES(password), group_id=VALUES(group_id)
                ''', (user["uid"], user["user_id"], user["name"], user["privilege"], user["password"], user["group_id"]))

                # Insertar o actualizar huellas
                for fingerprint in user["fingerprints"]:
                    template_binario = fingerprint["template"]
                    cursor.execute('''  
                        INSERT INTO huellas (user_uid, finger_id, template)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        template = VALUES(template)
                    ''', (user["uid"], fingerprint["finger_id"], template_binario))

        conexion.commit()
    finally:
        conexion.close()

def crear_respaldo():
    try:
        # Conectar al reloj checador
        conn = checador.connect()
        if not conn:
            return {"error": "No se pudo conectar al reloj checador"}

        # Deshabilitar el dispositivo
        conn.disable_device()

        # Obtener información de los usuarios
        usuarios = conn.get_users()
        if not usuarios:
            return {"error": "No se encontraron usuarios en el reloj checador"}

        respaldo = []
        for user in usuarios:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'

            user_data = {
                "uid": user.uid,
                "user_id": user.user_id,
                "name": user.name,
                "privilege": privilege,
                "password": user.password,
                "group_id": user.group_id,
                "fingerprints": []
            }

            # Obtener huellas digitales
            for finger_id in range(10):  # Asumiendo máximo 10 huellas por usuario
                try:
                    finger = conn.get_user_template(uid=user.uid, temp_id=finger_id)
                    if finger and finger.template:
                        template_data = finger.template
                        
                        # Asegurar que el template sea bytes
                        if isinstance(template_data, str):
                            template_data = template_data.encode('utf-8')

                        user_data["fingerprints"].append({
                            "finger_id": finger_id,
                            "template": template_data
                        })
                except Exception as e:
                    sys.stderr.write(f"Error al obtener huella {finger_id} del usuario {user.user_id}: {e}\n")

            respaldo.append(user_data)

        # Guardar en base de datos
        guardar_en_base_datos(respaldo)

        # Habilitar dispositivo nuevamente
        conn.enable_device()
        conn.disconnect()

        return {"status": "Respaldo creado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        inicializar_base_datos()
        resultado = crear_respaldo()
        print(json.dumps(resultado))  # Imprimir solo el JSON como salida
    except Exception as e:
        print(json.dumps({"error": str(e)}))