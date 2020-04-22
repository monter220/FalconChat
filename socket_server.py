from socket import *
from threading import Thread
import json
import datetime


def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print('%s:%s has connected.' % client_address)
        client.send(bytes('Type your name and press enter!', 'utf8'))
        address = '%s:%s' % (client_address[0], client_address[1])
        addresses[address] = client
        Thread(target=start_client, args=(client, address)).start()


def start_client(client, address):
    today = datetime.datetime.today()
    msg = client.recv(1024).decode('utf8')
    print(msg)    #for test
    msg = json.loads(msg)
    print(msg)     #for test
    for send_name in msg:
        name = msg[send_name]
    print(clients)    #for test
    name_correct = True
    while True:
        for i in clients:
            if name == clients[i]:
                name_correct = False
                client.send(bytes('User with the same name already exists', 'utf8'))
                client.send(bytes('Type your name and press enter!', 'utf8'))
                msg = client.recv(1024).decode('utf8')
                msg = json.loads(msg)
                for send_name in msg:
                    name = msg[send_name]
                break
            else:
                name_correct = True
        if name_correct:
            break

    client.send(bytes('Welcome %s!' % name, 'utf8'))
    msg = '%s has joined the chat!' % name
    broadcast(bytes(msg, 'utf8'))
    clients[address] = name
    client.send(bytes(json.dumps(clients), 'utf8'))
    print(clients) #for test

    while True:
        msg = client.recv(1024).decode('utf8')
        msg = json.loads(msg)
        for send_name in msg:
            if send_name != '' and send_name != 'All' and send_name != 'All chat clients':
                name_not_found = True
                while True:
                    for send_address in clients:
                        if send_name == clients[send_address]:
                            name_not_found = False
                            if name != send_name:
                                addresses[send_address].send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + name +
                                                                   '->Me: ' + msg[send_name], 'utf8'))
                                client.send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + name +
                                                  '->' + send_name + ': ' + msg[send_name], 'utf8'))
                            else:
                                client.send(bytes('I don’t know why you did it, but...', 'utf8'))
                                client.send(bytes('[' + today.strftime("%H:%M:%S") + '] Me->Me: '
                                                  + msg[send_name], 'utf8'))
                            break
                        else:
                            name_not_found = True
                    if name_not_found:
                        client.send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + send_name + ' not found', 'utf8'))
                        break
                    break
            else:
                msg = bytes(msg[send_name], 'utf8')
                if msg != bytes('[{esc}]', 'utf8') and msg != bytes('[{reload_clients}]', 'utf8'):
                    broadcast(msg, name + ': ')
                elif msg == bytes('[{reload_clients}]', 'utf8'):
                    client.send(bytes(json.dumps(clients), 'utf8'))
                    client.send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + 'client list updated', 'utf8'))
                else:
                    del clients[address]
                    print(clients)  #for test
                    broadcast(bytes('%s has left the chat.' % name, 'utf8'))
                    client.close()
                    break


def broadcast(msg, prefix=''):
    today = datetime.datetime.today()
    for client in clients:
        addresses[client].send(bytes('[' + today.strftime("%H:%M:%S") + '] ' + prefix, 'utf8') + msg)


clients = {}
addresses = {}

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('', 21090))

if __name__ == "__main__":
    SERVER.listen(100)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()