import argparse

parser = argparse.ArgumentParser()
parser.add_argument("nm", type = str)
parser.add_argument("id", type = int)
parser.add_argument("pvg", type = str)
parser.add_argument("ip", type = str) 
args = parser.parse_args()

from zk import ZK,const

conn = None
zk = ZK(args.ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    #print ('Connecting to device ...')
    conn = zk.connect()
    #print ('Disabling device ...')
    conn.disable_device()
    #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
    users = conn.get_users()
    maxid= args.id
    for user in users:
        if int(user.user_id) == maxid:
            maxid=int(user.user_id)
            #print(maxid)
            maxid2 = str(maxid)
            print (args.pvg)
            if args.pvg == "User":
                conn.set_user(uid= maxid, name= args.nm, privilege=args.pvg, password= '', group_id='', user_id=maxid2, card=0)
            elif args.pvg == "Admin":
                conn.set_user(uid= maxid, name= args.nm, privilege=const.USER_ADMIN, password= '', group_id='', user_id=maxid2, card=0)

    #print ('Enabling device ...')
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()