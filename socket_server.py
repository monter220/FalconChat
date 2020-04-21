from socket import *
from threading import Thread
import time
import json


def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print('%s:%s has connected.' % client_address)
        client.send(bytes('Type your name and press enter!', 'utf8'))
        address = '%s:%s' % (client_address[0], client_address[1])
        addresses[address] = client
        Thread(target=start_client, args=(client, address)).start()


def start_client(client, address):
    name = client.recv(1024).decode('utf8')
    client.send(bytes('[' + time.ctime() + '] ' + 'Welcome %s!' % name, 'utf8'))
    msg = '%s has joined the chat!' % name
    broadcast(bytes('[' + time.ctime() + '] ' + msg, 'utf8'))
    clients[address] = name
    client.send(bytes(json.dumps(clients), 'utf8'))

    while True:
        msg = client.recv(1024)
        if msg != bytes('[{esc}]', 'utf8') and msg != bytes('[{reload_clients}]', 'utf8'):
            broadcast(msg, name + ': ')
        elif msg == bytes('[{reload_clients}]', 'utf8'):
            client.send(bytes(json.dumps(clients), 'utf8'))
        else:
            client.send(bytes('[{esc}]', 'utf8'))
            client.close()
            del clients[client]
            broadcast(bytes('[' + time.ctime() + '] ' + '%s has left the chat.' % name, 'utf8'))
            break


def broadcast(msg, prefix=''):
    for client in clients:
        addresses[client].send(bytes('[' + time.ctime() + '] ' + prefix, 'utf8') + msg)


clients = {}
addresses = {}

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('', 21090))

if __name__ == "__main__":
    SERVER.listen()
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()