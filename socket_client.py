from socket import *
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf8')
            msg_list.insert(tkinter.END, msg)

        except OSError:
            break


def send(event=None):
    msg = new_msg.get()
    new_msg.set("")
    client_socket.send(bytes(msg, 'utf8'))
    if msg == '[{esc}]':
        esc()


def esc(event=None):
    msg = '[{esc}]'
    client_socket.send(bytes(msg, 'utf8'))
    client_socket.close()
    top.quit()


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

new_msg = tkinter.StringVar()
new_msg.set('Put your name here')
entry_field = tkinter.Entry(textvariable=new_msg)
entry_field.bind('<Return>', send)
entry_field.pack(side=tkinter.LEFT)
send_button = tkinter.Button(text='Send', command=send)
send_button.pack(side=tkinter.LEFT)
quit_button = tkinter.Button(text='esc', command=esc)
quit_button.pack(side=tkinter.LEFT)

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