#-*- coding: utf-8 -*-

import sys
import argparse                         #Imports para argumentos y funciones del tiempo
from datetime import datetime
parser = argparse.ArgumentParser()
args = parser.parse_args()
sys.path.append("zk")

from zk import ZK   #Import de la carpeta ZK con los archivos relacionados

conn = None
#ip=args.ip
zk = ZK('192.168.1.200', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)   #Reemplazo de la ip y los parametros de la conexión

try:
    #print ('Connecting to device ...')
    conn = zk.connect() #Conexión con el dispositivo y mensaje de confirmación
    #print ('Disabling device ...')
    conn.disable_device() #Dehabilitar el dispositivo y mensaje de confirmación
    #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))

    conn.clear_attendance()
   
    #print ('Enabling device ...')   
    conn.enable_device()            #Rehabilitación del dispositivo y mensaje de confirmación
except Exception as e:
    print ("Process terminate : {}".format(e))  #Final de las funciones y mensjae de confirmación
    
finally:
    if conn:
        conn.disconnect()      #Desconexión del dispositivo