from socket import *
from threading import Thread
import json
import datetime
import time
import configparser
from cryptography.fernet import Fernet


def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print('%s:%s has connected.' % client_address)
        address = '%s:%s' % (client_address[0], client_address[1])
        Thread(target=start_client, args=(client, address)).start()


def start_client(client, address):
    today = datetime.datetime.today()
    client_msg = client.recv(RRR).decode('utf8')
    msg = decrypt(client_msg)
    name = msg[list(msg.keys())[0]]
    name_correct = True
    while True:
        for clients_name in clients:
            if name == clients_name:
                name_correct = False
                client.send(encrypt('Falcon with the same name already exists'))
                time.sleep(1)
                client.send(encrypt('Type your name in msg line and press enter!'))
                client_msg = client.recv(RRR).decode('utf8')
                msg = decrypt(client_msg)
                name = msg[list(msg.keys())[0]]
                break
            else:
                name_correct = True
        if name_correct:
            break

    client.send(encrypt('Welcome %s!' % name))
    msg = '%s landed!' % name
    broadcast(msg)
    clients[name] = client
    time.sleep(1)
    reload_clients()

    while True:
        client_msg = client.recv(RRR).decode('utf8')
        msg = decrypt(client_msg)
        send_name = list(msg.keys())[0]
        if send_name != '' and send_name != 'All falcons':
            name_not_found = True
            while True:
                for client_name in clients:
                    if send_name == client_name:
                        name_not_found = False
                        if name != send_name:
                            clients[client_name].send(encrypt('[' + today.strftime("%H:%M:%S") + '] ' + name +
                                                              '->Me: ' + msg[send_name]))
                            client.send(encrypt('[' + today.strftime("%H:%M:%S") + '] Me->' + send_name +
                                                ': ' + msg[send_name]))
                        else:
                            client.send(encrypt('I don’t know why you did it, but...'))
                            client.send(encrypt('[' + today.strftime("%H:%M:%S") + '] Me->Me: ' + msg[send_name]))
                        break
                if name_not_found:
                    client.send(encrypt('[' + today.strftime("%H:%M:%S") + '] ' + send_name + ' not found'))
                    break
                break
        else:
            msg_to_send = msg[send_name]
            if msg_to_send != '[{esc}]':
                client.send(encrypt('[' + today.strftime("%H:%M:%S") + '] Me: ' + msg_to_send))
                broadcast_without_address(name, msg_to_send, name + ': ')
            else:
                del clients[name]
                broadcast('%s flew away.' % name)
                reload_clients()
                client.close()
                break


def broadcast(msg, prefix=''):
    today = datetime.datetime.today()
    for client in clients:
        if client != 'All falcons':
            clients[client].send(encrypt('[' + today.strftime("%H:%M:%S") + '] ' + prefix + msg))


def broadcast_without_address(name, msg, prefix=''):
    today = datetime.datetime.today()
    for client in clients:
        if name != client:
            if client != 'All falcons':
                clients[client].send(encrypt('[' + today.strftime("%H:%M:%S") + '] ' + prefix + msg))


def reload_clients():
    for client in clients:
        if client != 'All falcons':
            clients[client].send(encrypt(json.dumps({'reload_clients': list(clients.keys())})))


def decrypt(msg):
    client_crypt_msg = json.loads(msg)
    client_cipher = Fernet(bytes(list(client_crypt_msg.keys())[0], 'utf8'))
    msg = json.loads(client_cipher.decrypt(bytes(client_crypt_msg[list(client_crypt_msg.keys())[0]], 'utf8')).decode('utf8'))
    return msg


def encrypt(server_msg):
    client_msg = bytes(server_msg, 'utf8')
    crypt_msg = server_cipher.encrypt(client_msg)
    send_crypt_msg = {server_key.decode('utf8'): crypt_msg.decode('utf8')}
    msg = bytes(json.dumps(send_crypt_msg), 'utf8')
    return msg


clients = {'All falcons': ''}

RRR = 1024
server_key = Fernet.generate_key()
server_cipher = Fernet(server_key)

SERVER = socket(AF_INET, SOCK_STREAM)

config = configparser.ConfigParser()
config.read('socket_server.ini')

IP_ADD = config['SETTING']['IP_ADD']
PORT = int(config['SETTING']['PORT'])

SERVER.bind((IP_ADD, PORT))

if __name__ == "__main__":
    SERVER.listen(100)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()