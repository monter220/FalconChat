import socket

data = None
sock = socket.socket()
sock.connect(('localhost', 21090))

data = input('Message:')

while data != "quite":
    sock.send(bytes(data, "utf8"))
    data = sock.recv(1024)
    print(data)
    data = input('Message:')

print('Disconnect...')

sock.close()