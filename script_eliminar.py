import argparse                             #importa las funciones para los argumentos que serviran para los scrips

parser = argparse.ArgumentParser() 
parser.add_argument("x", type = int)
parser.add_argument("ip", type = str) #se agrega y se de clara la variable que funcioara como argumeto 
args = parser.parse_args()                  # funcion para los argumentos


from zk import ZK                          #referencia la clase de la libreria zk  y importa Zk

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    #print ('Connecting to device ...')
    conn = zk.connect()

    #print ('Disabling device ...')
    conn.disable_device()

    #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
    users = conn.get_users()

    #Eliminación de usuarios por ID        
    conn.delete_user(user_id=args.x)            #funcionm para eliminar el registro de usuario mediate el uid

    #print ('Enabling device ...')
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()