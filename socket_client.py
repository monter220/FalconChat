from socket import *
from threading import Thread
import tkinter
import json


def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf8')
            if msg.find('{"reload_clients":') != -1:
                msg = json.loads(msg)
                client_list.delete(0, tkinter.END)
                msg = msg['reload_clients']
                for i in msg:
                    print(i)
                    client_list.insert(0, i)
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    msg = new_msg.get()
    new_msg.set("")
    if msg == '[{esc}]':
        esc()
    else:
        if client_list.curselection().__len__() == 0:
            send_name = 'All chat clients'
        else:
            send_name = client_list.get(client_list.curselection()[0])
        send_msg = {send_name: msg}
        msg = json.dumps(send_msg)
        client_socket.send(bytes(msg, 'utf8'))


def esc(event=None):
    msg = '[{esc}]'
    send_msg = {'': msg}
    msg = json.dumps(send_msg)
    client_socket.send(bytes(msg, 'utf8'))
    client_socket.close()
    top.quit()


top = tkinter.Tk()
top.title('Test')

messages_frame = tkinter.Frame()
scrollbar = tkinter.Scrollbar(messages_frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
client_list = tkinter.Listbox(messages_frame, height=15, width=25)
client_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

new_msg = tkinter.StringVar()
new_msg.set('Put your name here')

quit_button = tkinter.Button(text='esc', command=esc)
quit_button.pack(side=tkinter.RIGHT)
send_button = tkinter.Button(text='Send', command=send)
send_button.pack(side=tkinter.RIGHT)

entry_field = tkinter.Entry(textvariable=new_msg)
entry_field.bind('<Return>', send)
entry_field.pack(side=tkinter.RIGHT)

top.protocol('WM_DELETE_WINDOW', esc)

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