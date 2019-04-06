import socket
import pickle
import random

class NetworkUDP:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = "127.0.0.1"  # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
        # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
        # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:

            self.client.sendto(pickle.dumps(data), self.addr)
            data_rec, addr_rec = self.client.recvfrom(1024)  # buffer size is 1024 bytes
            return pickle.loads(data_rec)
        except socket.error as e:
            return str(e)


# UDP_IP = "127.0.0.1"
# UDP_PORT = 5555
# MESSAGE = "Hello, World!"
#
# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
# data,addr = sock.recvfrom(2048)
# print(data.decode())
N = NetworkUDP()

for e in range(0,10):
    data_to_send = {'uid': "1234", "x": random.randint(0,1024), 'y': random.randint(0,768)}
    print(N.send(data_to_send))