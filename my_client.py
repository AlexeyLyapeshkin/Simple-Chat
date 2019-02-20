import socket
import pickle
import time
import threading

stop = False

def receving(sock):
    while not stop:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                unpick = pickle.loads(data)
                print('['+unpick['Name']+']:' + unpick['Message']+'\n')
                time.sleep(0.2)
        except:
            sock.close()


main_message = ' {0} is connected! '
left_message = ' {0} is left chat! '

host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.0.102", 9090)

channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
channel.bind((host, port))
channel.setblocking(1)

print('{0:-^51}'.format('[Client started]'))

print("Please, enter you name:")
nickname = input('>>> ')
print('-'*60)

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
        data = {'Name': nickname, 'Message': left_message.format(nickname),'Code':1}
        datapickle = pickle.dumps(data)
        channel.sendto(datapickle, server)

channel.close()
thread.join()
