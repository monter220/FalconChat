import socket

data = input('a:')


sock = socket.socket()
sock.connect(('localhost', 21090))
sock.send(bytes(data, "utf8"))

data = sock.recv(1024)
sock.close()


print(data)

