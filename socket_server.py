from socket import *
from threading import Thread
import json
import datetime
import time


def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print('%s:%s has connected.' % client_address)
        address = '%s:%s' % (client_address[0], client_address[1])
        Thread(target=start_client, args=(client, address)).start()


def start_client(client, address):
    today = datetime.datetime.today()
    msg = client.recv(1024).decode('utf8')
    msg = json.loads(msg)
    name = msg[list(msg.keys())[0]]
    name_correct = True
    while True:
        for clients_name in clients:
            if name == clients_name:
                name_correct = False
                client.send(bytes('Falcon with the same name already exists', 'utf8'))
                time.sleep(1)
                client.send(bytes('Type your name and press enter!', 'utf8'))
                msg = client.recv(1024).decode('utf8')
                msg = json.loads(msg)
                name = msg[list(msg.keys())[0]]
                break
            else:
                name_correct = True
        if name_correct:
            break

    client.send(bytes('Welcome %s!' % name, 'utf8'))
    msg = '%s landed!' % name
    broadcast(bytes(msg, 'utf8'))
    clients[name] = client
    time.sleep(1)
    reload_clients()

    while True:
        msg = client.recv(1024).decode('utf8')
        msg = json.loads(msg)
        send_name = list(msg.keys())[0]
        if send_name != '' and send_name != 'All falcons':
            name_not_found = True
            while True:
                for client_name in clients:
                    if send_name == client_name:
                        name_not_found = False
                        if name != send_name:
                            clients[client_name].send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + name +
                                                            '->Me: ' + msg[send_name], 'utf8'))
                            client.send(bytes('[' + today.strftime("%H:%M:%S") + '] Me->' +
                                              send_name + ': ' + msg[send_name], 'utf8'))
                        else:
                            client.send(bytes('I don’t know why you did it, but...', 'utf8'))
                            client.send(bytes('[' + today.strftime("%H:%M:%S") + '] Me->Me: '
                                              + msg[send_name], 'utf8'))
                        break
                if name_not_found:
                    client.send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + send_name + ' not found', 'utf8'))
                    break
                break
        else:
            msg_to_send = bytes(msg[send_name], 'utf8')
            if msg_to_send != bytes('[{esc}]', 'utf8'):
                client.send(bytes('[' + today.strftime("%H:%M:%S") + '] Me: ', 'utf8') + msg_to_send)
                broadcast_without_address(name, msg_to_send, name + ': ')
            else:
                del clients[name]
                broadcast(bytes('%s flew away.' % name, 'utf8'))
                reload_clients()
                client.close()
                break


def broadcast(msg, prefix=''):
    today = datetime.datetime.today()
    for client in clients:
        if client != 'All falcons':
            clients[client].send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + prefix, 'utf8') + msg)


def broadcast_without_address(name, msg, prefix=''):
    today = datetime.datetime.today()
    for client in clients:
        if name != client:
            if client != 'All falcons':
                clients[client].send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + prefix, 'utf8') + msg)


def reload_clients():
    for client in clients:
        if client != 'All falcons':
            clients[client].send(bytes(json.dumps({'reload_clients': list(clients.keys())}), 'utf8'))


clients = {'All falcons': ''}

SERVER = socket(AF_INET, SOCK_STREAM)

IP_add = input('IP_address: ')
PORT = input('port: ')
if not IP_add:
    IP_add = 'localhost'
if not PORT:
    PORT = 21090
else:
    PORT = int(PORT)
SERVER.bind((IP_add, PORT))

if __name__ == "__main__":
    SERVER.listen(100)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()