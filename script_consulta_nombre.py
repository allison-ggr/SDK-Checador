# -*- coding: utf-8 -*-
import sys         #Imports para los argumentos
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("nm", type = str)
parser.add_argument("ip", type = str) #Declaración de los argumentos
args = parser.parse_args()
sys.path.append("zk")

from zk import ZK, const    #Import de la carpeta ZK con los archivos relacionados

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)       #Reemplazo de la ip y los parametros de la conexión

try:        #Inicio del Try
    print ('Connecting to device ...')
    conn = zk.connect()                     #Conexión don el dispositivo y mensaje de confirmación
    print ('Disabling device ...')
    conn.disable_device()                    #Deshabilitación del dispositivo y mensaje
    print ('Firmware Version: : {}'.format(conn.get_firmware_version()))        #Información del Firmware
    # print '--- Get User ---'
    users = conn.get_users()            #Conección a las clases de Usuarios
    finger = conn.get_user_template()   #Conección a las clases de Huellas    
    
    for user in users:          #Inicio del ciclo
        privilege = 'User'           #Verificación del privilegio
        if user.privilege == const.USER_ADMIN:      #Verificación de privilegios de administrador
            privilege = 'Admin'         
        if user.user_id==args.nm:         #Comparación del User_ID del usuario y del argumento ingresado   
            print ('  Name       : {}'.format(user.name))      #Si el UID del usuario y el argumento coinciden consultar e imprimir el nombre del usuario

    print ('Enabling device ...')       #Rehabilitación del dispositivo y mensaje
    conn.enable_device()                
except Exception as e:          #Final del Try
    print ("Process terminate : {}".format(e))      #Final de los procesos
finally:
    if conn:
        conn.disconnect()   #Desconexión de los dispositivos 