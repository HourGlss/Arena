import socket


# class Network:
#
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.host = "127.0.0.1" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
#                                     # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
#                                     # ipv4 address. This feild will be the same for all your clients.
#         self.port = 5555
#         self.addr = (self.host, self.port)
#         self.id = self.connect()
#
#     def connect(self):
#         self.client.connect(self.addr)
#         return self.client.recv(2048).decode()
#
#     def send(self, data):
#         """
#         :param data: str
#         :return: str
#         """
#         try:
#             self.client.send(str.encode(data))
#             reply = self.client.recv(2048).decode()
#             return reply
#
#         except socket.error as e:
#             return str(e)

UDP_IP = "127.0.0.1"
UDP_PORT = 5555
MESSAGE = "Hello, World!"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
data,addr = sock.recvfrom(2048)
print(data.decode())
