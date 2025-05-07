# -*- coding: utf-8 -*-
import sys
import argparse
import json
from datetime import datetime
import pymysql
from zk import ZK, const

# Agregar carpeta de módulos
sys.path.append("zk")

# Argumentos del script
parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str, help="IP del checador")
args = parser.parse_args()

# Validación de IP
if args.ip == "192.168.1.200":
    checador_id = 10
else:
    print(json.dumps({"error": "IP no válida"}))
    sys.exit(1)

# Conexión al checador
zk = ZK(args.ip, port=4370, timeout=10, password=0, force_udp=False, ommit_ping=False)

# Conexión a la base de datos
db = pymysql.connect(
    host='192.168.1.175',
    user='authen',
    password='D3s@rr0ll02022',
    database='pruebaChecador'
)
cursor = db.cursor()

# Listas para reporte y guardado
registros_guardados = []
omitidos = []
errores = []

try:
    conn = zk.connect()
    conn.disable_device()
    attendances = conn.get_attendance()

    for attendance in attendances:
        user_id = attendance.user_id
        fecha = attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Verificar si el usuario existe
        cursor.execute("SELECT COUNT(*) FROM empleados WHERE id_usuario = %s", (user_id,))
        if cursor.fetchone()[0] == 0:
            omitidos.append({
                "usuario": user_id,
                "fecha": fecha,
                "motivo": "Usuario no existe"
            })
            continue

        # Verificar si el registro ya existe
        cursor.execute("""
            SELECT COUNT(*) FROM registros 
            WHERE fecha = %s AND id_usuario = %s AND id_checador = %s
        """, (fecha, user_id, checador_id))
        if cursor.fetchone()[0] > 0:
            omitidos.append({
                "usuario": user_id,
                "fecha": fecha,
                "motivo": "Registro duplicado"
            })
            continue

        # Insertar nuevo registro
        try:
            sql = "INSERT INTO registros (fecha, id_usuario, id_checador) VALUES (%s, %s, %s)"
            cursor.execute(sql, (fecha, user_id, checador_id))
            db.commit()
            registros_guardados.append({
                "usuario": user_id,
                "fecha": fecha,
                "checador_id": checador_id
            })
        except Exception as e:
            errores.append({
                "usuario": user_id,
                "fecha": fecha,
                "error": str(e)
            })
            db.rollback()

    # Guardar registros en archivo JSON local
    with open("registros_guardados.json", "w", encoding="utf-8") as f:
        json.dump(registros_guardados, f, indent=4, ensure_ascii=False)

   
    print(json.dumps({"status": "success"}, indent=4, ensure_ascii=False))

finally:
    if conn:
        conn.enable_device()
        conn.disconnect()
    cursor.close()
    db.close()
