from socket import *
from threading import Thread
import tkinter
import json


def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf8')
            if msg[0] == '{':
                msg = json.loads(msg)
                print(msg)                                      # for testing
                client_list.delete(0, tkinter.END)
                for i in msg:
                    print(i)
                    client_list.insert(0, msg[i])
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    msg = new_msg.get()
    new_msg.set("")
    send_name = new_destination.get()
    new_destination.set(send_name)
    send_msg = {send_name: msg}
    print(send_msg)
    msg = json.dumps(send_msg)
    client_socket.send(bytes(msg, 'utf8'))
    if msg == '[{esc}]':
        esc()
    elif msg == '[{reload_clients}]':
        update_clients_list()


def esc(event=None):
    msg = '[{esc}]'
    send_msg = {'': msg}
    msg = json.dumps(send_msg)
    client_socket.send(bytes(msg, 'utf8'))
    client_socket.close()
    top.quit()


def update_clients_list(event=None):
    msg = '[{reload_clients}]'
    send_msg = {'': msg}
    msg = json.dumps(send_msg)
    client_socket.send(bytes(msg, 'utf8'))


def If_window_close(event=None):
    new_msg.set('[{esc}]')
    send()


top = tkinter.Tk()
top.title('Test')

messages_frame = tkinter.Frame()
scrollbar = tkinter.Scrollbar(messages_frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
client_list = tkinter.Listbox(messages_frame, height=15, width=15)
client_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

client_update_button = tkinter.Button(text='Update clients-list', command=update_clients_list)
client_update_button.pack(side=tkinter.LEFT)

new_msg = tkinter.StringVar()
new_msg.set('Put your name here')

new_destination = tkinter.StringVar()
new_destination.set('All chat clients')

quit_button = tkinter.Button(text='esc', command=esc)
quit_button.pack(side=tkinter.RIGHT)
send_button = tkinter.Button(text='Send', command=send)
send_button.pack(side=tkinter.RIGHT)

entry_field = tkinter.Entry(textvariable=new_msg)
entry_field.bind('<Return>', send)
entry_field.pack(side=tkinter.RIGHT)

entry_destination = tkinter.Entry(textvariable=new_destination)
entry_destination.pack(side=tkinter.TOP)

top.protocol('WM_DELETE_WINDOW', If_window_close)

IP_add = input('Server_IP_address: ')
PORT = input('Server_port: ')
if not IP_add:
    IP_add = 'localhost'
else:
    IP_add = int(IP_add)
if not PORT:
    PORT = 21090
else:
    PORT = int(PORT)

connect = (IP_add, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(connect)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()