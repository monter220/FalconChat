import socket
import time
import threading


sock = socket.socket()
sock.bind(('', 21090))
sock.listen()


def answer(_conn):
    while True:
        data = str(_conn.recv(1024), "utf8")
        if not data:
            break
        _conn.send(bytes('[' + time.ctime() + '] ' + data.upper(), "utf8"))
    _conn.close()


while True:
    conn, addr = sock.accept()
    print('connected:', addr)
    t = threading.Thread(target=answer(conn))
    t.start()