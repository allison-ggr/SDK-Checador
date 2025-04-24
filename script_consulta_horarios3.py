
#-*- coding: utf-8 -*-
import sys
import argparse                         #Imports para argumentos y funciones del tiempo
from datetime import datetime
parser = argparse.ArgumentParser()
#parser.add_argument("id", type = str)   #Declaración de argumentos
#parser.add_argument("ip", type = str)  

#parser.add_argument("ip", type = str)   
args = parser.parse_args()
sys.path.append("zk")

from zk import ZK   #Import de la carpeta ZK con los archivos relacionados

conn = None

json='['
#ip=args.ip
zk = ZK("192.168.30.249", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión

try:
    #print ('Connecting to device ...')
    conn = zk.connect() #Conexión con el dispositivo y mensaje de confirmación
   
    #print ('Disabling device ...')
    conn.disable_device() #Dehabilitar el dispositivo y mensaje de confirmación 
    #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
   
    #users = conn.get_users() #Conección a las clases de Usuarios
    #finger = conn.get_user_template() #Conección a las clases de Horarios
    attendances = conn.get_attendance() #Conección a las clases de Huellas
    i=1 #Declaración de variables
    c=1
    nochecador=3
    #CHECADOR NUMERO 1
    for attendance in attendances:
        if attendance.user_id == attendance.user_id: #Recorrido de los marcajes segun el ID
            c=c+1   
    for attendance in attendances:  
        if attendance.user_id: #Recorrido de los horarios para comenzar con la cadena JSON           
            json=json+ '{"id_checador'+'":'+'"'+attendance.user_id+'","fecha"'+':'+attendance.timestamp.strftime('"%Y-%m-%d %H:%M:%S",')+'"no_checador":"'+str(nochecador)+'"},'
            if i == c-1:
                json=json+ '{"id_checador'+'":'+'"'+attendance.user_id+'","fecha"'+':'+attendance.timestamp.strftime('"%Y-%m-%d %H:%M:%S",')+'"no_checador":"'+str(nochecador)+'"}'    #Formato para hora y fecha
            i=i+1
    #print(consulta)
    #print ('Enabling device ...')   
    conn.enable_device()            #Rehabilitación del dispositivo y mensaje de confirmación
    json=json+']'  #Llave de cierre para el JSON
    print(json)
except Exception as e:
    print ("Error")  #Final de las funciones y mensjae de confirmación
    
finally:
    if conn:
        conn.disconnect()      #Desconexión del
