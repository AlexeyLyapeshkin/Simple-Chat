import socket
import pickle
import time
import threading
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


def receving(sock):
    stop = False
    while not stop:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                unpick = pickle.loads(data)
                print('[' + unpick['Name'] + ']: ' + unpick['Message'] + '\n')
                time.sleep(0.2)
        except:
            stop = True
            sock.close()


def main(ip, port):
    stop = False
    main_message = ' {0} is connected! '
    left_message = ' {0} is left chat! '


    server = (ip, port)

    channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    channel.bind((ip, 0))
    channel.setblocking(1)

    print('{0:-^51}'.format('[Client started]'))

    print("Please, enter you name:")
    nickname = input('>>> ')
    print('-' * 60)

    thread = threading.Thread(target=receving, args=[channel])
    thread.start()

    data = {'Name': nickname, 'Message': main_message.format(nickname)}
    datapickle = pickle.dumps(data)
    channel.sendto(datapickle, server)

    while not stop:
        try:
            message = input('\n')
            if message:
                data = {'Name': nickname, 'Message': message}
                datapickle = pickle.dumps(data)

                channel.sendto(datapickle, server)
            time.sleep(0.2)
        except:
            stop = True
            print('{0:-^51}'.format('[Client stoped]'))
            data = {'Name': nickname, 'Message': left_message.format(nickname), 'Code': 1}
            datapickle = pickle.dumps(data)
            channel.sendto(datapickle, server)
    channel.close()
    sys.exit()








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
