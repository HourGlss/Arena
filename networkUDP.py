import socket
import pickle
import random
import time
import config


class Network:
    uid = None
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = config.host_ip  # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
        # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
        # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)

    def set_uid(self, uid):
        self.uid = uid

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:

            self.client.sendto(pickle.dumps(data), self.addr)
            #TODO THIS MAY BE AN ISSUE, WE ARE WAITING TO RECEIVE A RESPONSE HERE. NOT IDEAL
            data_rec, addr_rec = self.client.recvfrom(1024)  # buffer size is 1024 bytes
            print("-",data_rec,addr_rec)
            dict_response = pickle.loads(data_rec)
            if self.uid is None:
                self.set_uid(dict_response[0]['uid'])
            return dict_response
        except socket.error as e:
            return str(e)

#FIRST POC
# UDP_IP = "127.0.0.1"
# UDP_PORT = 5555
# MESSAGE = "Hello, World!"
#
# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
# data,addr = sock.recvfrom(2048)
# print(data.decode())


#SECOND POC
# N = NetworkUDP()
# last_sent = None
# while True:
#     now = time.time()
#     if last_sent == None or now - last_sent >= .06:
#         data_to_send = {"x": random.randint(0, 1024), 'y': random.randint(0, 768),'mouse_x':random.randint(0, 768),'mouse_y':random.randint(0, 768)}
#         rec_data = N.send(data_to_send)
#         print("My UID is {}".format(rec_data[0]['uid']))
#         last_sent = now
