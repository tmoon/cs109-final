import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",8123))
print(s.getsockname()[0])
s.close()