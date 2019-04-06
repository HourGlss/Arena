import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

clients =[]

while True:
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print("received:{} from {}".format(data,addr))
    s.sendto("response".encode(),addr)