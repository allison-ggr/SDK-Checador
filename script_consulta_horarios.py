#-*- coding: utf-8 -*-
import sys
import argparse                         #Imports para argumentos y funciones del tiempo
from datetime import datetime
parser = argparse.ArgumentParser()
#parser.add_argument("id", type = str)   #Declaración de argumentos
#parser.add_argument("ip", type = str)   
args = parser.parse_args()
sys.path.append("zk")

from zk import ZK   #Import de la carpeta ZK con los archivos relacionados

conn = None
conn2 =None
conn3 =None
conn4 =None
conn5 =None

json='['
#ip=args.ip
zk = ZK("192.168.1.200", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión
zk2 = ZK("192.168.1.201", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión
zk3 = ZK("192.168.1.201", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión
zk4 = ZK("192.168.1.201", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión
zk5 = ZK("192.168.1.201", port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión
try:
    #print ('Connecting to device ...')
    conn = zk.connect() #Conexión con el dispositivo y mensaje de confirmación
    conn2 = zk2.connect() #Conexión con el dispositivo y mensaje de confirmación
    #print ('Disabling device ...')
    conn.disable_device() #Dehabilitar el dispositivo y mensaje de confirmación
    conn2.disable_device() #Dehabilitar el dispositivo y mensaje de confirmación
    
    #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
   
    #users = conn.get_users() #Conección a las clases de Usuarios
    #finger = conn.get_user_template() #Conección a las clases de Horarios
    attendances = conn.get_attendance() #Conección a las clases de Huellas
    attendances2 = conn2.get_attendance() #Conección a las clases de Huellas
    
    i=1 #Declaración de variables
    c=1
    nochecador=1
    #CHECADOR NUMERO 1
    for attendance in attendances:
        if attendance.user_id == attendance.user_id: #Recorrido de los marcajes segun el ID
            c=c+1   
    for attendance in attendances:  
        if attendance.user_id: #Recorrido de los horarios para comenzar con la cadena JSON           
            json=json+ '{"id_checador'+'":'+'"'+attendance.user_id+'","fecha"'+':'+attendance.timestamp.strftime('"%Y-%m-%d %H:%M:%S",')+'"no_checador":"'+str(nochecador)+'"},'    #Formato para hora y fecha
            i=i+1
    #CHEACDOR NUMERO 2
    i=1
    c=1
    nochecador=2
    for attendance in attendances2:
        if attendance.user_id == attendance.user_id: #Recorrido de los marcajes segun el ID
            c=c+1   
    for attendance in attendances2:  
        if attendance.user_id: #Recorrido de los horarios para comenzar con la cadena JSON           
            if i == c-1:
                json=json+ '{"id_checador'+'":'+'"'+attendance.user_id+'","fecha"'+':'+attendance.timestamp.strftime('"%Y-%m-%d %H:%M:%S",')+'"no_checador":"'+str(nochecador)+'"}'
            else:
                json=json+ '{"id_checador'+'":'+'"'+attendance.user_id+'","fecha"'+':'+attendance.timestamp.strftime('"%Y-%m-%d %H:%M:%S",')+'"no_checador":"'+str(nochecador)+'"},'    #Formato para hora y fecha
            
            i=i+1
    
    #print(consulta)
    #print ('Enabling device ...')   
    conn.enable_device()            #Rehabilitación del dispositivo y mensaje de confirmación
    conn2.enable_device()            #Rehabilitación del dispositivo y mensaje de confirmación
except Exception as e:
    print ("Process terminate : {}".format(e))  #Final de las funciones y mensjae de confirmación
    
finally:
    if conn:
        conn.disconnect()      #Desconexión del
    if conn2:
        conn2.disconnect()      #Desconexión del
json=json+']'  #Llave de cierre para el JSON
print(json)