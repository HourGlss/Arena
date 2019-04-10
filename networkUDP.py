import socket
import pickle
import random
import time
import config
import threading
import sys

class Network:
    uid = None
    sleep_time = .016
    to_send = None
    to_send_lock = False
    last_received = None
    last_received_lock = False
    def __init__(self):
        self.host = config.host_ip  # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
        # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
        # ipv4 address. This feild will be the same for all your clients.
        self.incoming_port = 5556
        self.outgoing_port = 5555
        self.incoming_addr = (self.host, self.incoming_port)
        self.outgoing_addr = (self.host, self.outgoing_port)
        outgoing = threading.Thread(target=self.outgoing)
        outgoing.start()
        incoming = threading.Thread(target=self.incoming)
        incoming.start()


    def set_uid(self, uid):
        self.uid = uid

    def incoming(self):
        incoming = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        incoming.bind(("", self.incoming_port))
        while True:
            if not self.last_received_lock:
                self.last_received_lock = True
                data_rec, addr_rec = incoming.recvfrom(1024)
                self.last_received = pickle.loads(data_rec)
                # print(data_rec)
                # print(self.last_received)
                if self.uid is None:
                    self.set_uid(self.last_received[0]['uid'])
                self.last_received_lock = False
                time.sleep(self.sleep_time)

    def outgoing(self):
        outgoing = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            if not self.to_send_lock:
                self.to_send_lock = True
                if self.to_send is not None:
                    # print("data was actually sent")
                    pickled = pickle.dumps(self.to_send)
                    print(sys.getsizeof(pickled))
                    outgoing.sendto(pickled, self.outgoing_addr)

                self.to_send_lock = False
                time.sleep(self.sleep_time)

    def send(self, data_to_send):
        if not self.to_send_lock:
            self.to_send_lock = True
            self.to_send = data_to_send
            self.to_send_lock = False
            return True
        return False

    def receive(self):
        # print("receive is being called")
        if not self.last_received_lock:
            self.last_received_lock = True
            # print("it's not locked")
            if self.last_received is not None:
                # print("It isnt none")
                data_to_return = self.last_received
                # print(data_to_return)
                self.last_received = None
            else:
                # print("It is none")
                self.last_received_lock = False
                return False
            self.last_received_lock = False
            return data_to_return
        return False
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
# N = Network()
# last_sent = None
# while True:
#     now = time.time()
#     if last_sent == None or now - last_sent >= .06:
#         data_to_send = {"x": random.randint(0, 1024), 'y': random.randint(0, 768),'mouse_x':random.randint(0, 768),'mouse_y':random.randint(0, 768)}
#         response = False
#         response = N.send(data_to_send)
#         if response:
#             # print("data was Qd to be sent")
#             pass
#         received = N.recieve()
#         if received != False:
#             # print("was received",received)
#             pass
#
#         # print("My UID is {}".format(N.uid))
#         last_sent = now
