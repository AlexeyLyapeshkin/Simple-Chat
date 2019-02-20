import socket, time
import pickle
import sys


def tester(host='192.168.0.102', port=9090):
    s = socket.socket()
    s.settimeout(5)
    answer = s.connect_ex((host, port))
    if answer == 10061:
        s.close()
        return True
    else:
        s.close()
        return False


def main(ip, port):
    stop = False
    print('{0:^20} - {1:^20}'.format(ip, port))
    clients = {}

    channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    channel.bind((ip, port))
    print('{0:-^51}'.format('[Server started]'))

    while not stop:
        try:
            # RECIVE DATA
            data, adr = channel.recvfrom(1024)
            unpick = pickle.loads(data)  # UNPACK DATA

            # NEW USERS
            if adr not in clients.values():
                clients[unpick['Name']] = adr

            try:
                if unpick['Code'] == 1:
                    del clients[unpick['Name']]
            except:
                pass

            if clients:
                for client in clients:
                    if clients[client] != adr:
                        channel.sendto(data, clients[client])
            # LOG
            itsatime = time.strftime("%Y.%m.%d - %H:%M:%S", time.localtime())
            print(
                "[" + adr[0] + "] - [" + str(adr[1]) + "] - [" + itsatime + "] - [" + unpick['Name'] + "] >> " + unpick[
                    'Message'], end="\n")
        except:
            print('{0:-^51}'.format('[Server stoped]'))
            stop = True





if __name__ == '__main__':
    if len(sys.argv) == 3:
        ip, port = sys.argv[1], sys.argv[2]
        if tester(ip, int(port)):
            main(ip, int(port))
        else:
            print('__LOCAL_MODE__')
            main('192.168.0.102', 9090)
    else:
        print('__LOCAL_MODE__')
        main('192.168.0.102', 9090)
