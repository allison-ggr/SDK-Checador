# -*- coding: utf-8 -*-
import sys
sys.path.append("zk")

from zk import ZK, const

conn = None
zk = ZK('192.168.1.200', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    print ('Connecting to device ...')
    conn = zk.connect()
    print ('Disabling device ...')
    conn.disable_device()
    print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
    # print '--- Get User ---'
    users = conn.get_users()
    fingers = conn.get_templates()
  
    
    
    #Tabla con las diferentes consultas 
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        print ('- UID #{}'.format(user.uid))
        print ('  Name       : {}'.format(user.name))
        print ('  Privilege  : {}'.format(privilege))
        print ('  Password   : {}'.format(user.password))
        print ('  Group ID   : {}'.format(user.group_id))
        print ('  User  ID   : {}'.format(user.user_id))
        #Consulta las huellas de los usuarios según su id
        print ('  Finger     : {}'.format(conn.get_user_template(uid= user.uid, temp_id=0)))
                
            
        #Crear usuario con (Nota: Privilegio debe asignarse como 'User')
        #conn.set_user(uid=1, name='Fanani M. Ihsan', privilege=const.USER_ADMIN, password='12345678', group_id='', user_id='123', card=0)

        #Eliminación de usuarios por ID        
        #conn.delete_user(user_id=123)
        
    #print ("Voice Test ...")
    #conn.test_voice()
    print ('Enabling device ...')
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
