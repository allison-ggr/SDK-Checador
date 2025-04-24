#-*- coding: utf-8 -*-
import sys
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

parser = argparse.ArgumentParser()
args = parser.parse_args()
sys.path.append("zk")

from zk import ZK

conn = None

json = '['
zk = ZK("192.168.1.200", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    conn = zk.connect()
    conn.disable_device()

    attendances = conn.get_attendance()
    users = conn.get_users()  # Obtener información de los usuarios
    user_dict = {user.user_id: user.name for user in users}  # Crear un diccionario de ID a nombres

    attendance_data = defaultdict(list)
    for attendance in attendances:
        user_id = attendance.user_id
        timestamp = attendance.timestamp
        attendance_data[user_id].append(timestamp)

    for user_id, timestamps in attendance_data.items():
        timestamps.sort()  # Ordenar las marcas de tiempo
        daily_data = defaultdict(list)

        # Agrupar marcas por día
        for timestamp in timestamps:
            date_key = timestamp.date()
            daily_data[date_key].append(timestamp)

        name = user_dict.get(user_id, "Desconocido")
        for date, day_timestamps in daily_data.items():
            day_timestamps.sort()
            total_hours = timedelta(0)

            # Procesar en bloques de 4 (2 entradas y 2 salidas)
            for i in range(0, len(day_timestamps), 4):
                if i + 3 < len(day_timestamps):  # Asegurarse de que haya 4 marcas
                    entrada1 = day_timestamps[i]
                    salida1 = day_timestamps[i + 1]
                    entrada2 = day_timestamps[i + 2]
                    salida2 = day_timestamps[i + 3]
                    hours_worked = (salida1 - entrada1) + (salida2 - entrada2)
                    total_hours += hours_worked

            json += '{"id_checador":"' + user_id + '","nombre":"' + name + '","fecha":"' + str(date) + '","horas_trabajadas":"' + str(total_hours) + '"},'

    json = json.rstrip(',') + ']' 
    print(json)

except Exception as e:
    print("Error:", e)

finally:
    if conn:
        conn.disconnect()