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
                print(msg)                                      # for testing
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
            send_name = 'All falcons'
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
    chat_window.quit()


def esc2(event=None):
    connect_window.destroy()
    quit()


def start_connect(event=None):
    __IP_add = ip_add_ins.get()
    __PORT = int(port_add_ins.get())
    if not __IP_add:
        __IP_add = 'localhost'
    if not __PORT:
        __PORT = 21090
    else:
        __PORT = int(__PORT)
    connect = (__IP_add, __PORT)
    client_socket.connect(connect)
    connect_window.destroy()


client_socket = socket(AF_INET, SOCK_STREAM)

connect_window = tkinter.Tk()
connect_window.title('Connection to FalconChat')
connect_window.geometry('400x250')

ip_add_pref = tkinter.Label(connect_window, text='Insert_server_ip_address:')
ip_add_pref.pack(side=tkinter.TOP, fill=tkinter.BOTH)
ip_add_ins = tkinter.StringVar(connect_window)
ip_add_ins.set('127.0.0.1')
ip_add_ins_field = tkinter.Entry(connect_window, textvariable=ip_add_ins)
ip_add_ins_field.pack(side=tkinter.TOP)

port_add_pref = tkinter.Label(connect_window, text='Insert_server_port:')
port_add_pref.pack(side=tkinter.TOP, fill=tkinter.BOTH)
port_add_ins = tkinter.StringVar(connect_window)
port_add_ins.set('21090')
port_add_ins_field = tkinter.Entry(connect_window, textvariable=port_add_ins)
port_add_ins_field.pack(side=tkinter.TOP)

connect_button = tkinter.Button(connect_window, text='Connect', command=start_connect)
connect_button.pack(side=tkinter.TOP)

connect_window.protocol('WM_DELETE_WINDOW', esc2)

connect_window.mainloop()

chat_window = tkinter.Tk()
chat_window.title('FalconChat')

messages_frame = tkinter.Frame(chat_window)
scrollbar = tkinter.Scrollbar(messages_frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
client_list = tkinter.Listbox(messages_frame, height=15, width=25)
client_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

new_msg = tkinter.StringVar(chat_window)
new_msg.set('Put your name here')

quit_button = tkinter.Button(chat_window, text='esc', command=esc)
quit_button.pack(side=tkinter.RIGHT)
send_button = tkinter.Button(chat_window, text='Send', command=send)
send_button.pack(side=tkinter.RIGHT)

entry_field = tkinter.Entry(chat_window, textvariable=new_msg)
entry_field.bind('<Return>', send)
entry_field.pack(side=tkinter.RIGHT)

chat_window.protocol('WM_DELETE_WINDOW', esc)

receive_thread = Thread(target=receive)
receive_thread.start()
chat_window.mainloop()