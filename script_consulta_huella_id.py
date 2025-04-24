# -*- coding: utf-8 -*-
import sys         #Imports para los argumentos
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("id", type = str)   #Declaración de los argumentos
parser.add_argument("ip", type = str) 
args = parser.parse_args()
sys.path.append("zk")

from zk import ZK, const    #Import de la carpeta ZK con los archivos relacionados

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión

try:    #Inicio del Try
    print ('Connecting to device ...')
    conn = zk.connect()                     #Conexión don el dispositivo y mensaje de confirmación
    print ('Disabling device ...')
    conn.disable_device()                   #Deshabilitación del dispositivo y mensaje
    print ('Firmware Version: : {}'.format(conn.get_firmware_version()))    #Información del Firmware
  
    users = conn.get_users()            #Conección a las clases de Usuarios
    finger = conn.get_user_template()   #Conección a las clases de Huellas
    
    for user in users:         #Inicio del ciclo
        privilege = 'User'      #Verificación del privilegio
        if user.privilege == const.USER_ADMIN:  #Verificación de privilegios de administrador
            privilege = 'Admin'
        if user.user_id==args.id:   #Comparación del argumento ingresado y del User_ID del Usuario
            print (' finger    : {}'.format(conn.get_user_template( user_id = args.id, temp_id=0)))   #Si la información de usuario es correcta consultar e imprimir la hulla del usuario 
    print ('Enabling device ...')
    conn.enable_device()            #Rehabilitación del dispositivo y mensaje
except Exception as e:      #Final del Try
    print ("Process terminate : {}".format(e))  #Final de la funciones
finally:
    if conn:
        conn.disconnect()   #Desconexión del dispositivo