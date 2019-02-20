import socket,time
import pickle

host = socket.gethostbyname(socket.gethostname())
port = 9090


clients = {}

channel = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
channel.bind((host,port))
print('{0:-^51}'.format('[Server started]'))
log_file = open('LOG.txt','w')
stop = False
while not stop:
    try:
        # RECIVE DATA
        data, adr = channel.recvfrom(1024)
        unpick = pickle.loads(data) # UNPACK DATA


        # NEW USERS
        if adr not in clients.values():
            clients[unpick['Name']] = adr

        try:
            if unpick['Code'] == 1:
                del clients[unpick['Name']]
        except KeyError:
            pass

        if clients:
            for client in clients:
                if clients[client] != adr:
                    channel.sendto(data,clients[client])
        else:
            pass

        # LOG
        itsatime = time.strftime("%Y.%m.%d - %H:%M:%S", time.localtime())
        print("[" + adr[0] + "] - [" + str(adr[1]) + "] - [" + itsatime + "] - [" + unpick['Name'] + "] >> "+unpick['Message'], end="\n")
        time.sleep(0.1)
    except KeyboardInterrupt:
        print('{0:-^51}'.format('[Server stoped]'))
        stop = True


channel.close()