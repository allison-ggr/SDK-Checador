import json
from zk import ZK

# Configuración de los checadores
checadors = [
    {"ip": "192.168.1.200", "id": 1},
    {"ip": "192.168.1.201", "id": 2}
]

# Listas para almacenar los datos
horarios = []
usuarios = []

for checador in checadors:
    zk = ZK(checador["ip"], port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = None
    try:
        print(f"Conectando al checador {checador['id']} ({checador['ip']})...")
        conn = zk.connect()
        conn.disable_device()

        # Obtener horarios
        print(f"Obteniendo horarios del checador {checador['id']}...")
        attendances = conn.get_attendance()
        for attendance in attendances:
            horarios.append({
                "id_checador": attendance.user_id,
                "fecha": attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "no_checador": checador["id"]
            })

        # Obtener usuarios y huellas
        print(f"Obteniendo usuarios y huellas del checador {checador['id']}...")
        users = conn.get_users()
        for user in users:
            usuario = {
                "id_checador": checador["id"],
                "user_id": user.user_id,
                "name": user.name,
                "privilege": user.privilege,
                "password": user.password,
                "group_id": user.group_id,
                "templates": []
                }
            for finger_id in range(10):  # Suponiendo un máximo de 10 huellas por usuario
                template = conn.get_user_template(uid=user.uid, temp_id=finger_id)
                if template:
                    usuario["templates"].append({
                    "finger_id": finger_id,
                    "template": str(template)  # Convertir el objeto a cadena
                    })
                    usuarios.append(usuario)

        print(f"Datos obtenidos del checador {checador['id']}.")

    except Exception as e:
        print(f"Error al conectar con el checador {checador['id']}: {e}")
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()

# Guardar los horarios en un archivo JSON
with open("horarios.json", "w", encoding="utf-8") as archivo_horarios:
    json.dump(horarios, archivo_horarios, indent=4, ensure_ascii=False)
print("Horarios guardados en 'horarios.json'.")

# Guardar los usuarios y sus huellas en un archivo JSON
with open("usuarios_y_huellas.json", "w", encoding="utf-8") as archivo_usuarios:
    json.dump(usuarios, archivo_usuarios, indent=4, ensure_ascii=False)
print("Usuarios y huellas guardados en 'usuarios_y_huellas.json'.")